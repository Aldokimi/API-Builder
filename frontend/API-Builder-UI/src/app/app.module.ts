import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AuthModule } from './auth/auth.module';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MainPageComponent } from './main-page/main-page.component';
import { NavBarComponent } from './nav-bar/nav-bar.component';
import { CookieModule } from 'ngx-cookie';
import { UserModule } from './profiles/user.module';
import { PagenotfoundComponent } from './shared/pagenotfound/pagenotfound.component';
import { ProjectsComponent } from './projects/projects.component';
import { NewProjectFormComponent } from './projects/new-project-form/new-project-form.component';

@NgModule({
  declarations: [
    AppComponent,
    MainPageComponent,
    NavBarComponent,
    PagenotfoundComponent,
    ProjectsComponent,
    NewProjectFormComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    AuthModule,
    ReactiveFormsModule,
    CookieModule.withOptions(),
    UserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
