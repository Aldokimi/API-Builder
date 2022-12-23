import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RegisterPageComponent } from './register-page/register-page.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LoginPageComponent } from './login-page/login-page.component';
import { RouterModule } from '@angular/router';
import { HttpClient, HttpClientModule, HttpClientXsrfModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { IsAuthenticatedGuard } from './guards/is-authenticated.guard';
import { AuthInterceptorProvider } from './interceptors/auth.interceptor';


@NgModule({
  declarations: [
    RegisterPageComponent,
    LoginPageComponent
    
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule,
    HttpClientModule,
    HttpClientXsrfModule
  ],
  providers: [HttpClient,IsAuthenticatedGuard,AuthInterceptorProvider],
  bootstrap: []
})
export class AuthModule { }
