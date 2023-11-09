import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Equipment } from './equipment.model';
import { EquipmentType } from './equipmentType.model';
@Injectable({
  providedIn: 'root'
})
export class EquipmentService {
  constructor(http: HttpClient) {}

  /** Returns all equipment entries from backend database table using backend HTTP get request
   * @returns {Observable<Equipment[]>}
   */
  getAllEquipment(): Equipment[] {
    let equipment1: Equipment = {
      id: '123456',
      model: 'Quest 3',
      isCheckedOut: false,
      imgURL: './../../../assets/Oculus-csxl-sp00.png'
    };
    let equipment2: Equipment = {
      id: '54321',
      model: 'Ipad1',
      isCheckedOut: false,
      imgURL: './../../../assets/Oculus-csxl-sp00.png'
    };
    let equipment3: Equipment = {
      id: '123456',
      model: 'Quest 4',
      isCheckedOut: false,
      imgURL: './../../../assets/Oculus-csxl-sp00.png'
    };
    let equipment4: Equipment = {
      id: '54321',
      model: 'Ipad2',
      isCheckedOut: false,
      imgURL: './../../../assets/Oculus-csxl-sp00.png'
    };
    let equipment5: Equipment = {
      id: '123456',
      model: 'Quest 6',
      isCheckedOut: false,
      imgURL: './../../../assets/Oculus-csxl-sp00.png'
    };
    let equipment6: Equipment = {
      id: '54321',
      model: 'Ipad3',
      isCheckedOut: false,
      imgURL: './../../../assets/Oculus-csxl-sp00.png'
    };
    let equipment7: Equipment = {
      id: '123456',
      model: 'Quest 5',
      isCheckedOut: false,
      imgURL: './../../../assets/Oculus-csxl-sp00.png'
    };
    let equipment8: Equipment = {
      id: '54321',
      model: 'Ipad4',
      isCheckedOut: false,
      imgURL: './../../../assets/Oculus-csxl-sp00.png'
    };
    return [
      equipment1,
      equipment2,
      equipment3,
      equipment4,
      equipment5,
      equipment6,
      equipment7,
      equipment8
    ];
  }

  /** Returns the equipment object from the backend database table using backend HTTP get request.
   * @returns {Observable<Equipment>}
   */
  getSingleEquipment(id: string): Equipment {
    let equipment1: Equipment = {
      id: '123456',
      model: 'Quest 3',
      isCheckedOut: false,
      imgURL: './../../../assets/Oculus-csxl-sp00.png'
    };
    return equipment1;
  }

  /** Returns an array containing an array of equipment types present from calling getAllEquipment()
   * This is necessary to display available equipment as it looks in the wireframe.
   * @returns {Observable<EquipmentType[]>}
   */
  transformToEquipmentType(): EquipmentType[] {
    let equipment: Equipment[] = this.getAllEquipment();
    var equipmentTypes: EquipmentType[] = [];

    for (var item of equipment) {
      let model = item.model;
      let imgURL = item.imgURL;

      //check if equipmentypes[] contains that equipment type

      //does not contain that type of equipment
      if (!(equipmentTypes.filter((e) => e.model === model).length > 0)) {
        //check if the item is checked out
        if (item.isCheckedOut === true) {
          let equipmentType: EquipmentType = {
            model: model,
            numAvailable: 0,
            imgURL: imgURL
          };
          equipmentTypes.push(equipmentType);
        } else {
          let equipmentType: EquipmentType = {
            model: model,
            numAvailable: 1,
            imgURL: imgURL
          };
          equipmentTypes.push(equipmentType);
        }
      }
      //equipmentypes[] contains that equipmentType
      else if (!item.isCheckedOut) {
        //find object with matching model
        const equipmentToChange = equipmentTypes.find(
          (e) => e.model === item.model
        );

        //if object was found(should be true)
        if (equipmentToChange) {
          //modify object to add 1 to numAvailable
          equipmentToChange.numAvailable += 1;
        }
      }
    }
    return equipmentTypes;
  }
}
