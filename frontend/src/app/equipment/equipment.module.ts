import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserEquipmentComponent } from './user-equipment/user-equipment.component';
import { EquipmentCard } from './widgets/equipment-card/equipment-card.widget';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { EquipmentService } from './equipment.service';
@NgModule({
  //  eslint-disable-next-line prettier/prettier
  declarations: [UserEquipmentComponent, EquipmentCard],
  imports: [CommonModule, MatCardModule, MatButtonModule],
  providers: [EquipmentService]
})
export class EquipmentModule {}
export { MatCardModule };
export { MatButtonModule };
