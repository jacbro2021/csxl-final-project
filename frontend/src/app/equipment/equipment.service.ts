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
}
