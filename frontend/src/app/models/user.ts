export class User {

  public id: number;
  public first_name: string;
  public last_name: string;
  public email: string;
  public password: string;

  constructor(data: any = null) {
    if (data) {
      this.id = data.id;
      this.first_name = data.first_name;
      this.last_name = data.last_name;
      this.email = data.email;
    }
  }

  public toJSON(): any {
    return {
      id: this.id,
      first_name: this.first_name,
      last_name: this.last_name,
      email: this.email,
      password: this.password
    }
  }
}