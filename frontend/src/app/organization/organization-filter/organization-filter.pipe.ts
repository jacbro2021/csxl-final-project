/**
 * This is the pipe used to filter organizations on the organizations page.
 * 
 * @author Jade Keegan
 * @copyright 2023
 * @license MIT
 */

import { Pipe, PipeTransform } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Organization } from '../organization.service';

@Pipe({
  name: 'organizationFilter'
})
export class OrganizationFilterPipe implements PipeTransform {

  /** Returns a mapped array of organizations that start with the input string (if search query provided). 
   * @param {Observable<Organization[]>} organizations: observable list of valid Organization models
   * @param {String} searchQuery: input string to filter by
   * @returns {Observable<Organization[]>}
   */
  transform(organizations: Observable<Organization[]>, searchQuery: String): Observable<Organization[]> {
    // Sort the organizations list alphabetically by name
    organizations = organizations.pipe(
      map(orgs => orgs.sort((a: Organization, b: Organization) => {
        return a.name.toLowerCase().localeCompare(b.name.toLowerCase());
      }))
    )

    // If a search query is provided, return the organizations that start with the search query.
    if (searchQuery) {
      return organizations.pipe(
        map(organizations => organizations
          .filter(organization =>
            organization.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            organization.short_description.toLowerCase().includes(searchQuery.toLowerCase()) ||
            organization.long_description.toLowerCase().includes(searchQuery.toLowerCase()))));
    } else {
      // Otherwise, return the original list.
      return organizations;
    }
  }

}