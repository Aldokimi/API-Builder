import {
  async,
  ComponentFixture,
  fakeAsync,
  TestBed,
} from '@angular/core/testing';
import { UntypedFormBuilder } from '@angular/forms';
import { AppModule } from 'src/app/app.module';
import { AuthService } from '../services/auth.service';
import { RegisterPageComponent } from './register-page.component';
import { validUser, blankUser } from './../../../mocks/registerMock';
import { Router } from '@angular/router';

const registerServiceSpy = jasmine.createSpyObj('AuthService', ['register']);
const routerSpy = jasmine.createSpyObj('Router', ['navigateByUrl']);

describe('RegisterPageComponent', () => {
  let component: RegisterPageComponent;
  let fixture: ComponentFixture<RegisterPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppModule],
      declarations: [RegisterPageComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RegisterPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

describe('Register Component Isolated Test', () => {
  let component: RegisterPageComponent;
  let fixture: ComponentFixture<RegisterPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RegisterPageComponent],
      imports: [AppModule],
      providers: [AuthService],
    }).compileComponents();
    component = new RegisterPageComponent(
      new UntypedFormBuilder(),
      registerServiceSpy,
      new Router()
    );
  });

  function updateForm(
    username: string,
    userEmail: string,
    userPassword: string
  ) {
    component.my_register_form.controls['username'].setValue(username);
    component.my_register_form.controls['email'].setValue(userEmail);
    component.my_register_form.controls['password'].setValue(userPassword);
  }

  beforeEach(() => {
    fixture = TestBed.createComponent(RegisterPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('component initial state', () => {
    expect(component.submitted).toBeFalsy();
    expect(component.my_register_form).toBeDefined();
    expect(component.my_register_form.invalid).toBeTruthy();
    expect(component.errorOccured).toBeFalsy();
    expect(component.API_message).toBeUndefined();
  });

  it('submitted should be true when onRegisterSubmit() with valid user', () => {
    updateForm(validUser.username, validUser.email, validUser.password);
    component.onRegisterFormSubmit();
    expect(component.submitted).toBeTruthy();
    expect(component.errorOccured).toBeFalsy();
  });

  it('form value should update from when u change the input', () => {
    updateForm(validUser.username, validUser.email, validUser.password);
    expect(component.my_register_form.value).toEqual(validUser);
  });

  it('Form invalid should be true when form is invalid', () => {
    updateForm(blankUser.username, blankUser.email, blankUser.password);
    expect(component.my_register_form.invalid).toBeTruthy();
  });
});

describe('Register Component Shallow Test', () => {
  let fixture: ComponentFixture<RegisterPageComponent>;
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppModule],
      // providers: [
      //   {provide: AuthService, useValue: loginServiceSpy},
      //   UntypedFormBuilder,
      //   { provide: Router, useValue: routerSpy }
      // ],
      providers: [AuthService],
      declarations: [RegisterPageComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RegisterPageComponent);
    fixture.detectChanges();
    fixture.componentInstance.ngOnInit();
  });

  function updateForm(Email: string, userPassword: string) {
    fixture.componentInstance.my_register_form.controls['email'].setValue(
      Email
    );
    fixture.componentInstance.my_register_form.controls['password'].setValue(
      userPassword
    );
  }

  it('created a form with username and password input and register button', () => {
    // const fixture = TestBed.createComponent(LoginComponent);
    const emailContainer = fixture.debugElement.nativeElement.querySelector(
      '#username-container'
    );
    const passwordContainer = fixture.debugElement.nativeElement.querySelector(
      '#password-container'
    );
    const loginBtnContainer = fixture.debugElement.nativeElement.querySelector(
      '#register-btn-container'
    );
    expect(emailContainer).toBeDefined();
    expect(passwordContainer).toBeDefined();
    expect(loginBtnContainer).toBeDefined();
  });

  it('Disable form when email  is is blank', () => {
    updateForm(blankUser.email, validUser.password);

    fixture.detectChanges();

    // const emailErrorMsg = fixture.debugElement.nativeElement.querySelector('#email-error');

    // expect(emailErrorMsg).toBeDefined();
    expect(fixture.componentInstance.my_register_form.valid).toBeFalsy();
    expect(fixture.componentInstance.my_register_form.status).toBe('INVALID');
  });

  it('Disable form  when password is invalid', () => {
    updateForm(validUser.email, blankUser.password);
    fixture.detectChanges();

    expect(fixture.componentInstance.my_register_form.valid).toBeFalsy();
    expect(fixture.componentInstance.my_register_form.status).toBe('INVALID');
  });

  it('disble form when both email & Password are invalid', () => {
    updateForm(blankUser.email, blankUser.password);
    fixture.detectChanges();

    fixture.detectChanges();
    expect(fixture.componentInstance.my_register_form.valid).toBeFalsy();
    expect(fixture.componentInstance.my_register_form.status).toBe('INVALID');
  });
});
