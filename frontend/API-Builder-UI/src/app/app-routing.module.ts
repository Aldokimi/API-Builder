import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MainPageComponent } from './main-page/main-page.component';
import { RegisterPageComponent } from './auth/register-page/register-page.component';
import { LoginPageComponent } from './auth/login-page/login-page.component';
import { ProfileComponent } from './profiles/profile/profile.component';
import { IsAuthenticatedGuard } from './auth/guards/is-authenticated.guard';
import { PagenotfoundComponent } from './shared/pagenotfound/pagenotfound.component';
import { NewProjectFormComponent } from './projects/new-project-form/new-project-form.component';
import { AppComponent } from './app.component';


export const routes: Routes = [
  {
    path: "",
    component: MainPageComponent,
    //canActivate: [IsAuthenticatedGuard]

  },
  {
    path: "home",
    component: MainPageComponent,
    //canActivate: [IsAuthenticatedGuard]

  },
  {
    path: "projects",
    component: MainPageComponent,
    canActivate: [IsAuthenticatedGuard]
  },
  {
    path: "register",
    component: RegisterPageComponent,
    //canActivate: [IsAuthenticatedGuard]

  },
  {
    path: "login",
    component: LoginPageComponent,
    //canActivate: [IsAuthenticatedGuard]
  },
  {
    path: `profiles/:id`,
    component: ProfileComponent,
    canActivate: [IsAuthenticatedGuard]
  },
  {
    path: `profiles/:id/projects/new-project`,
    component: NewProjectFormComponent,
    canActivate: [IsAuthenticatedGuard]
  },
  {
    path: `profiles/:id/projects`,
    component: NewProjectFormComponent,
    canActivate: [IsAuthenticatedGuard]
  },
  {
    path: `profiles/:id/projects/:pId`,
    component: ProfileComponent,
    canActivate: [IsAuthenticatedGuard]
  },
  //Wild Card Route for 404 request
  { path: '**', pathMatch: 'full', 
  component: PagenotfoundComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
