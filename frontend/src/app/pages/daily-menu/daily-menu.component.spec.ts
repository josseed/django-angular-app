import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ValidateEmailComponent } from './validate-email.component';
import { NgZorroAntdModule } from 'ng-zorro-antd';
import { ActivatedRoute } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('ValidateEmailComponent', () => {
  let component: ValidateEmailComponent;
  let fixture: ComponentFixture<ValidateEmailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ValidateEmailComponent ],
      imports: [ NgZorroAntdModule, RouterTestingModule, HttpClientTestingModule ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ValidateEmailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
