import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProfileComponent } from './profile/profile.component';
import { ProfilesComponent } from './profiles/profiles.component';
//import { NewProjectFormComponent } from './new-project-form/new-project-form.component';

@NgModule({
  declarations: [ProfileComponent, ProfilesComponent],
  imports: [CommonModule],
})
export class UserModule {}
