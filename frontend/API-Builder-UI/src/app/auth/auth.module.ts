import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RegisterPageComponent } from './register-page/register-page.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LoginPageComponent } from './login-page/login-page.component';

@NgModule({
  declarations: [
    RegisterPageComponent,
    LoginPageComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    
  ],
  providers: [],
  bootstrap: []
})
export class AuthModule { }
