import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MainPageComponent } from './main-page/main-page.component';
import { RegisterPageComponent } from './auth/register-page/register-page.component';
import { LoginPageComponent } from './auth/login-page/login-page.component';
import { IsAuthenticatedGuard } from './auth/guards/is-authenticated.guard';


const routes: Routes = [
  {
    path: "",
    component: MainPageComponent,
    canActivate: [IsAuthenticatedGuard]

  },
  {
    path: "home",
    component: MainPageComponent,
    canActivate: [IsAuthenticatedGuard]

  },
  {
    path: "myprojects",
    component: MainPageComponent,
    canActivate: [IsAuthenticatedGuard]
  },
  {
    path: "register",
    component: RegisterPageComponent
  },
  {
    path: "login",
    component: LoginPageComponent
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
