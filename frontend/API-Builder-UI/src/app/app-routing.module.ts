import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MainPageComponent } from './main-page/main-page.component';
import { RegisterPageComponent } from './auth/register-page/register-page.component';


const routes: Routes = [
  {
    path: "",
    component: MainPageComponent
  },
  {
    path: "register",
    component: RegisterPageComponent
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
