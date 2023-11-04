import { Component } from '@angular/core';

@Component({
  selector: 'app-user-equipment',
  templateUrl: './user-equipment.component.html',
  styleUrls: ['./user-equipment.component.css']
})
export class UserEquipmentComponent {
  public static Route = {
    path: 'user-equipment',
    title: 'User Equipment Checkout',
    component: UserEquipmentComponent
  };
}
