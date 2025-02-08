export interface IAuthUser {
  id: number;
  email: string;
  is_oauth: boolean;
  is_superuser: boolean;
  last_login_at: string;
  oauth_provider: null;
  phone_number: string;
  role_id: null;
  status: string;
  username: string;
}
