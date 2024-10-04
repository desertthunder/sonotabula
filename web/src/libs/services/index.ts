import axios, { AxiosInstance, AxiosResponse } from "axios";
import { BASE_URL } from "./constants";

class NotImplementedError extends Error {
  constructor() {
    super("Method not implemented");
  }
}

export abstract class Service {
  private baseUrl: string;

  constructor(protected readonly client: AxiosInstance) {
    this.baseUrl = BASE_URL;
  }

  get baseURL() {
    if (!this.baseUrl) {
      throw new Error("Base URL is not set");
    }

    return this.baseUrl;
  }

  abstract fetch<T>(url: string): Promise<T>;

  abstract post<T>(url: string, data: Record<string, string>): Promise<T>;

  abstract put<T>(url: string, data: Record<string, string>): Promise<T>;
}

export interface IAuthService {
  login: (data: Record<string, string>) => Promise<void>;
  signup: (data: Record<string, string>) => Promise<void>;
}

type SimpleResponse = {
  redirect?: string;
};

export class AuthService extends Service implements IAuthService {
  public static build(): AuthService {
    const client = axios.create({
      baseURL: `${BASE_URL}/api`,
    });

    return new AuthService(client);
  }

  async login(_data: Record<string, string> = {}) {
    const data = await this.post<SimpleResponse>("/login", _data);

    if (data.redirect) {
      window.location.href = data.redirect;
    }
  }

  async signup(data: Record<string, string>) {
    await this.post("/signup", data);
  }

  async validateToken(jwt: string): Promise<boolean> {
    try {
      await this.client.post(
        "/validate",
        {},
        {
          headers: {
            Authorization: `Bearer ${jwt}`,
          },
        }
      );

      return true;
    } catch (error) {
      console.error(error);

      return false;
    }
  }

  async fetch<T>(_url: string): Promise<T> {
    throw new NotImplementedError();
  }

  async post<SimpleResponse>(
    url: string,
    data: Record<string, string>
  ): Promise<SimpleResponse> {
    const resp = await this.client.post<
      SimpleResponse,
      AxiosResponse<SimpleResponse>
    >(url, data);

    return resp.data as SimpleResponse;
  }

  async put<T>(url: string, data: Record<string, string>): Promise<T> {
    return this.client.put(url, data).then((res) => res.data);
  }
}

export const authService = AuthService.build();
