import {
  async,
  ComponentFixture,
  fakeAsync,
  TestBed,
} from '@angular/core/testing';
import { UntypedFormBuilder } from '@angular/forms';
import { AppModule } from 'src/app/app.module';
import { AuthService } from '../services/auth.service';
import { LoginPageComponent } from './login-page.component';
import { validUser, blankUser } from './../../../mocks/loginMock';

const loginServiceSpy = jasmine.createSpyObj('AuthService', ['login']);
const routerSpy = jasmine.createSpyObj('Router', ['navigateByUrl']);

describe('LoginPageComponent', () => {
  let component: LoginPageComponent;
  let fixture: ComponentFixture<LoginPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppModule],
      declarations: [LoginPageComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LoginPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

describe('Login Component Isolated Test', () => {
  let component: LoginPageComponent;
  let fixture: ComponentFixture<LoginPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [LoginPageComponent],
      imports: [AppModule],
      providers: [AuthService],
    }).compileComponents();
    component = new LoginPageComponent(
      new UntypedFormBuilder(),
      loginServiceSpy,
      routerSpy
    );
  });

  function updateForm(userEmail: string, userPassword: string) {
    component.my_login_form.controls['email'].setValue(userEmail);
    component.my_login_form.controls['password'].setValue(userPassword);
  }

  beforeEach(() => {
    fixture = TestBed.createComponent(LoginPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('component initial state', () => {
    expect(component.submitted).toBeFalsy();
    expect(component.my_login_form).toBeDefined();
    expect(component.my_login_form.invalid).toBeTruthy();
    expect(component.errorOccured).toBeFalsy();
    expect(component.API_message).toBeUndefined();
  });

  it('submitted should be true when onLoginSubmit() with valid user', () => {
    updateForm(validUser.email, validUser.password);
    component.onLoginFormSubmit();
    expect(component.submitted).toBeTruthy();
    expect(component.errorOccured).toBeFalsy();
  });

  it('form value should update from when u change the input', () => {
    updateForm(validUser.email, validUser.password);
    expect(component.my_login_form.value).toEqual(validUser);
  });

  it('Form invalid should be true when form is invalid', () => {
    updateForm(blankUser.email, blankUser.password);
    expect(component.my_login_form.invalid).toBeTruthy();
  });
});

describe('Login Component Shallow Test', () => {
  let fixture: ComponentFixture<LoginPageComponent>;
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppModule],
      // providers: [
      //   {provide: AuthService, useValue: loginServiceSpy},
      //   UntypedFormBuilder,
      //   { provide: Router, useValue: routerSpy }
      // ],
      providers: [AuthService],
      declarations: [LoginPageComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LoginPageComponent);
    fixture.detectChanges();
    fixture.componentInstance.ngOnInit();
  });

  function updateForm(Email: string, userPassword: string) {
    fixture.componentInstance.my_login_form.controls['email'].setValue(Email);
    fixture.componentInstance.my_login_form.controls['password'].setValue(
      userPassword
    );
  }

  it('created a form with username and password input and login button', () => {
    // const fixture = TestBed.createComponent(LoginComponent);
    const emailContainer = fixture.debugElement.nativeElement.querySelector(
      '#username-container'
    );
    const passwordContainer = fixture.debugElement.nativeElement.querySelector(
      '#password-container'
    );
    const loginBtnContainer = fixture.debugElement.nativeElement.querySelector(
      '#login-btn-container'
    );
    expect(emailContainer).toBeDefined();
    expect(passwordContainer).toBeDefined();
    expect(loginBtnContainer).toBeDefined();
  });

  it('Disable form when email  is is blank', () => {
    updateForm(blankUser.email, validUser.password);

    fixture.detectChanges();

    fixture.debugElement.nativeElement.querySelector('#login-btn').click();
    fixture.detectChanges();

    // const emailErrorMsg = fixture.debugElement.nativeElement.querySelector('#email-error');
    fixture.detectChanges();

    // expect(emailErrorMsg).toBeDefined();
    expect(fixture.componentInstance.my_login_form.valid).toBeFalsy();
    expect(fixture.componentInstance.my_login_form.status).toBe('INVALID');
  });

  it('Disable form  when password is invalid', () => {
    updateForm(validUser.email, blankUser.password);
    fixture.detectChanges();

    fixture.debugElement.nativeElement.querySelector('#login-btn').click();
    fixture.detectChanges();

    expect(fixture.componentInstance.my_login_form.valid).toBeFalsy();
    expect(fixture.componentInstance.my_login_form.status).toBe('INVALID');
  });

  it('disble form when both email & Password are invalid', () => {
    updateForm(blankUser.email, blankUser.password);
    fixture.detectChanges();

    fixture.debugElement.nativeElement.querySelector('#login-btn').click();
    fixture.detectChanges();
    expect(fixture.componentInstance.my_login_form.valid).toBeFalsy();
    expect(fixture.componentInstance.my_login_form.status).toBe('INVALID');
  });
});
