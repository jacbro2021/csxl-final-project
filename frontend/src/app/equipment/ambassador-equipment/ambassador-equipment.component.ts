import { Component, OnInit, ViewChild } from '@angular/core';
import { Route, Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { EquipmentService } from '../equipment.service';
import { CheckoutRequestModel } from '../checkoutRequest.model';
import { Observable, reduce, tap, timer } from 'rxjs';
import { StagedCheckoutRequestModel } from '../staged-checkout-request.model';
import { StageCard } from '../widgets/staged-checkout-request-card/staged-checkout-request-card.widget';
import { CheckoutRequestCard } from '../widgets/checkout-request-card/checkout-request-card.widget';

@Component({
  selector: 'app-ambassador-equipment',
  templateUrl: './ambassador-equipment.component.html',
  styleUrls: ['./ambassador-equipment.component.css']
})
export class AmbassadorEquipmentComponent implements OnInit {
  public static Route: Route = {
    path: 'ambassador',
    component: AmbassadorEquipmentComponent,
    title: 'XL Equipment',
    canActivate: [permissionGuard('equipment.update', 'equipment')],
    resolve: { profile: profileResolver }
  };

  checkoutRequests$: Observable<CheckoutRequestModel[]>;
  checkoutRequestsLength: number = 0;
  stagedCheckoutRequests: StagedCheckoutRequestModel[];

  @ViewChild(StageCard) stageTable: StageCard | undefined;
  @ViewChild(CheckoutRequestCard) requestTable: StageCard | undefined;

  constructor(
    public router: Router,
    private equipmentService: EquipmentService
  ) {
    this.checkoutRequests$ = equipmentService.getAllRequest();
    this.getCheckoutRequestLength();
    this.stagedCheckoutRequests = [];
  }

  // every 5 seconds call the get all request service method to update ambassador equipment checkout page.
  ngOnInit(): void {
    timer(0, 5000)
      .pipe(
        tap(
          (_) =>
            (this.checkoutRequests$ = this.equipmentService.getAllRequest())
        )
      )
      .subscribe();
  }

  updateCheckoutRequestsTable() {
    //updates the checkout request table
    this.checkoutRequests$ = this.equipmentService.getAllRequest();
    this.getCheckoutRequestLength();
    this.requestTable?.refreshTable();
  }

  approveRequest(request: CheckoutRequestModel) {
    // Remove the request from database table for checkin requests to prevent it from going back into check in request table on periodic update.
    this.cancelRequest(request);

    // Update checkout request table.
    this.updateCheckoutRequestsTable();
    this.requestTable?.refreshTable();
    // Convert request into staged request.
    let stagedRequest: StagedCheckoutRequestModel = {
      user_name: request.user_name,
      pid: request.pid,
      model: request.model,
      id_choices: [],
      selected_id: null
    };

    // Populate id_options for staged request
    let equipment_list = this.equipmentService.getAllEquipmentByModel(
      stagedRequest.model
    );
    equipment_list.subscribe({
      next(equipment_arr) {
        equipment_arr.forEach((item) => {
          stagedRequest.id_choices?.push(item.equipment_id);
        });
      },
      complete: () => {
        this.stagedCheckoutRequests.push(stagedRequest);
        this.getCheckoutRequestLength();
        this.stageTable?.refreshTable();
      }
    });
  }

  cancelRequest(request: CheckoutRequestModel) {
    // Calls the proper API route to remove a request from checkout requests table in the backend.
    this.equipmentService.deleteRequest(request).subscribe();
    this.updateCheckoutRequestsTable();
  }

  approveStagedRequest(request: StagedCheckoutRequestModel) {
    // Calls the proper API route to move request into checkouts table in backend.
    this.equipmentService.approveRequest(request); //DO NOT FORGET TO SUBSCRIBE
  }

  // Gets the length of the observable array of checkout request models.
  getCheckoutRequestLength() {
    this.checkoutRequests$
      .pipe(
        reduce((count) => count + 1, 1) // Starts with 0 and increments by 1 for each item
      )
      .subscribe((count) => (this.checkoutRequestsLength = count));
  }
}