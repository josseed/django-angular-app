import { Worker } from './worker';
export class Order {

  public id: number;
  public worker: Worker;
  public customization: string;

  constructor(data: any = null) {
    if (data) {
      this.id = data.id;
      if (data.worker) {
        this.worker = new Worker(data.worker);
      }
      this.customization = data.customization;
    }
  }
}