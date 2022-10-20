import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
@Component({
  selector: 'app-register-page',
  templateUrl: './register-page.component.html',
  styleUrls: ['./../../../assets/css-js-login-signup/my-login.less']
})
export class RegisterPageComponent implements OnInit {

  constructor(private fb: UntypedFormBuilder) { }
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

    console.log(form.controls);

  }



toggleFieldTextType() {
  this.fieldTextType = !this.fieldTextType;
}

}
