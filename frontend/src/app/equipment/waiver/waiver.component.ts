import { Component, ViewChild } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { EquipmentService } from '../equipment.service';
import { Router } from '@angular/router';
import {
  FormControl,
  FormGroupDirective,
  NgForm,
  Validators
} from '@angular/forms';
import { ErrorStateMatcher } from '@angular/material/core';

@Component({
  selector: 'app-equipment-waiver',
  templateUrl: './waiver.component.html',
  styleUrls: ['./waiver.component.css']
})
export class WaiverComponent {
  public static Route = {
    path: 'waiver',
    title: 'Sign Waiver',
    component: WaiverComponent
  };
  //Used to check to see if signature field is not empty
  formControl = new FormControl('', [Validators.required]);
  matcher = new ErrorStateMatcher();

  onSubmit() {
    //EquipmentService.updateWaiverStatus();        //TOD: implement this method in equipment service to update waiver completed field for user
  }

  constructor(
    equipmentService: EquipmentService,
    public router: Router
  ) {}
}
