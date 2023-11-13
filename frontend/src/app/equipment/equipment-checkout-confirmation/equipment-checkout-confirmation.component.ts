import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-equipment-checkout-confirmation',
  templateUrl: './equipment-checkout-confirmation.component.html',
  styleUrls: ['./equipment-checkout-confirmation.component.css']
})
export class EquipmentCheckoutConfirmationComponent {
  public static Route = {
    path: 'checkout',
    title: 'Checkout Confirmation',
    component: EquipmentCheckoutConfirmationComponent
  };

  constructor(public router: Router) {}
}
