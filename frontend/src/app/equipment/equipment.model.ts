/**
 * The Equipment Model defines the shape of Equipment data
 * retrieved from the Equipment Service and API.
 */

export interface Equipment {
  id: string;
  model: string;
  isCheckedOut: boolean;
}
