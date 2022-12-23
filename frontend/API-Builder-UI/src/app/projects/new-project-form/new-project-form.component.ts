import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/auth/services/auth.service';
import { ProjectServiceService } from '../project-service.service';

@Component({
  selector: 'app-new-project-form',
  templateUrl: './new-project-form.component.html',
  styleUrls: ['./new-project-form.component.less']
})
export class NewProjectFormComponent implements OnInit {

  constructor(private fb: UntypedFormBuilder, private authService : AuthService, private router:Router,private projectService: ProjectServiceService) { }
  my_project_form!: UntypedFormGroup;
  API_message! :string
  submitted = false;
  errorOccured = false;
  isLoading = false;
  fieldTextType: boolean = false;

  ngOnInit(): void {
  
    
  
   // this.projectService.getProjects();
  
    this.my_project_form
    = this.fb.group({
      projectname: ['New Project', Validators.required],
      type: ['json', [Validators.required]],
      content: ['', [Validators.required]],
    });

  }

  createNewProject(): void {
    this.API_message = '';
    this.isLoading = true;
    this.submitted = true;
    console.log(this.my_project_form.controls);
    
    // this.authService.register(this.my_project_form.get('projectname')?.value,this.my_project_form.get('type')?.value, this.my_project_form.get('content')?.value)
    // .subscribe(
    //   () => {
    //   this.isLoading = false;
    //   }
    //   ,(errorRes) => {
    //     this.isLoading =false;
    //     if(errorRes.error?.email)
    //         {this.API_message = errorRes.error?.email.join(', ');}
    //     else if(errorRes.error?.username)
    //     {this.API_message = errorRes.error?.email.username(', ');}
    //     else{
    //       this.API_message = "Unknown Error, Please try again later.";
    //     }
    //     console.log(errorRes.error)}
    // )

  }



toggleFieldTextType() {
  this.fieldTextType = !this.fieldTextType;
}

}
