export class Meal {

  public id: number;
  public name: string;

  constructor(data: any = null) {
    if (data) {
      this.id = data.id;
      this.name = data.name;
    }
  }

  public toJSON(): any {
    return {
      id: this.id,
      name: this.name
    }
  }
}