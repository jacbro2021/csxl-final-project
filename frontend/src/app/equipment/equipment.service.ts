import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Equipment } from './equipment.model';
import { EquipmentType } from './equipmentType.model';
@Injectable({
  providedIn: 'root'
})
export class EquipmentService {
  constructor(private http: HttpClient) {}

  /** Returns all equipment entries from backend database table using backend HTTP get request
   * @returns {Observable<Equipment[]>}
   */
  getAllEquipment(): Observable<Equipment[]> {
    return this.http.get<Equipment[]>('/api/equipment/get_all');
  }

  /** Returns all equipmentType objects from backend method using HTTP get request.
   * @returns {Observable<EquipmentType[]>}
   */
  getAllEquipmentTypes(): Observable<EquipmentType[]> {
    return this.http.get<EquipmentType[]>('/api/equipment/get_all_types');
  }
}
