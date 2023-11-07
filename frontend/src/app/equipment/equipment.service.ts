import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Equipment } from './equipment.model';
@Injectable({
  providedIn: 'root'
})
export class EquipmentService {
  constructor(http: HttpClient) {}

  /** Returns all equipment entries from backend database table using backend HTTP get request.
   * @returns {Observable<Equipment[]>}
   */
  getAllEquipment(): Equipment[] {
    let equipment1: Equipment = {
      id: '123456',
      model: 'Quest 3',
      isCheckedOut: false
    };
    let equipment2: Equipment = {
      id: '54321',
      model: 'Quest 3',
      isCheckedOut: false
    };
    return [equipment1, equipment1];
  }

  /** Returns the equipment object from the backend database table using backend HTTP get request.
   * @returns {Observable<Equipment>}
   */
  getSingleEquipment(id: string): Equipment {
    let equipment1: Equipment = {
      id: '123456',
      model: 'Quest 3',
      isCheckedOut: false
    };
    return equipment1;
  }

  trasnformAvailableToMap(): Map<String, number> {
    let equipment: Equipment[] = this.getAllEquipment();

    var equipmentMap = new Map<string, number>();

    for (var item of equipment) {
      const model = item.model;
      if (item.isCheckedOut === false) {
        if (!equipmentMap.has(item.model)) {
          equipmentMap.set(model, 1);
        } else {
          equipmentMap.set(model, equipmentMap.get(model)! + 1);
        }
      }
    }
    return equipmentMap;
  }
}
