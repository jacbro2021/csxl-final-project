import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UserEquipmentComponent } from './user-equipment/user-equipment.component';
import { WaiverComponent } from './waiver/waiver.component';
import { EquipmentCheckoutConfirmationComponent } from './equipment-checkout-confirmation/equipment-checkout-confirmation.component';
const routes: Routes = [
  UserEquipmentComponent.Route,
  WaiverComponent.Route,
  EquipmentCheckoutConfirmationComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EquipmentRoutingModule {}
