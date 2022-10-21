import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { AuthService } from '../services/auth.service';
@Component({
  selector: 'app-register-page',
  templateUrl: './register-page.component.html',
  styleUrls: ['./../../../assets/css-js-login-signup/my-login.less']
})
export class RegisterPageComponent implements OnInit {

  constructor(private fb: UntypedFormBuilder, private authService : AuthService) { }
  my_register_form!: UntypedFormGroup;

  
  isLoading = false;
  fieldTextType: boolean = false;

  ngOnInit(): void {
    this.my_register_form = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
    });

  }

  onRegisterFormSubmit(form: UntypedFormGroup): void {
    this.isLoading = true;
    this.authService.register(this.my_register_form.get('username')?.value,this.my_register_form.get('email')?.value, this.my_register_form.get('password')?.value)
      .subscribe((response) => {
        console.log(response);
         this.isLoading = false; 
      })
  }



toggleFieldTextType() {
  this.fieldTextType = !this.fieldTextType;
}

}
