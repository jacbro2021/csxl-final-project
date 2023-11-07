/**
 * The Equipment Card widget abstracts the implementation of each
 * individual equipment card from the whole equipment page.
 */

import { Component, Input } from '@angular/core';
import { Equipment } from '../../equipment.model';

@Component({
  selector: 'equipment-card',
  templateUrl: './equipment-card.widget.html',
  styleUrls: ['./equipment-card.widget.css']
})
export class EquipmentCard {
  /** Inputs and outputs go here */
  // @Input() equipment!: Equipment;
  /** Constructor */
  constructor() {}
}
