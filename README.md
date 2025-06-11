- docker compose up

# Keycloak

- Visit http://localhost:8080/ and login with `admin`/`admin`

- Click on `Manage realms` -> `Create realm` -> Realm name: `prp` -> `Create`

- Click on `Realm roles` -> `Create role` -> Role name: `PRP-Admin`

- Click on `Clients` -> `Create client`
    Client type: `OpenID Connect`
    Client ID: `prpId`
    Name: `prp-client`
    Authentication flow: `Standard flow`
    Valid redirect URIs: `http://localhost:8000/callback`

# Authentik

- Visit: http://localhost:9000/if/flow/initial-setup/
  Register with: `admin@authentik.com` / `password`

- Visit http://localhost:9000/if/admin/#/identity/users
  Create user with:
    Username: `user123`
    Nome: `User123`
    Tipo di utent: `Interno`
    Email: `user123@authentik.com`
    Percorso: users
  Click on the new user an then on `Imposta password`: `userpassword`
  
- Visit http://localhost:9000/if/admin/#/core/providers
  and click on `Crea` -> `OAuth2/OpenId Provider`:
    Nome: `prp`
    Flusso di autorizzazione: `default-provider-authorization-explicit-consent`
    Tipologia di client: `Confidenziale`
    Client ID: `clientId`
    Client Secret: `clientSecret`
    Reindirizzamento: `http://localhost:8080/realms/prp/broker/prp/endpoint`

- Visit http://localhost:9000/if/admin/#/core/applications and click `Crea`
    Nome: `PRP`
    Slug: `prp`
    Provider: `prp`
    Modalità motore criter: `any`


# Keycloak (again)

- Visit http://localhost:8080/ 
- Click on `Manage realms` and then `prp`
- Click on `Idetity provider` -> `OpenID Connect v1.0`
    Alias: `prp`
    Display name: `Login with Authentik`
    Discovery endpoint: `http://authentik-server-1:9000/application/o/prp/.well-known/openid-configuration`
    Client ID: `clientId`
    Client Secret: `clientSecret`


---

Right now we have no user in Keycloak (see http://localhost:8080/admin/master/console/#/prp/users)

- Open an incognito browser window and visit http://localhost:8000/

- Click `Login`

- Click `Login with Authentik`

- Login with `user123@authentik.com` / `userpassword`

- Click `Continua`

- Register for the first time in Keycloak
    Username: `foo`
    Email: `foo@bar.com`
    First name: `Foo`
    Last name: `Bar`

  🚨 **NOTE**: we'd like to avoid this and get info directly from Authentik

- See this
  ```
  Token Response
  {
      "exp": 1749647262,
      "iat": 1749646962,
      "auth_time": 1749646962,
      "jti": "onrtac:4e3b8107-0c3b-41a4-9589-8761a0f7bb36",
      "iss": "http://localhost:8080/realms/prp",
      "aud": "account",
      "sub": "7b904c8e-b574-4840-ab80-88fecb36dcc3",
      "typ": "Bearer",
      "azp": "prpId",
      "sid": "c39bbff5-7b42-4c81-999f-7be8cdfc9183",
      "acr": "1",
      "allowed-origins": [
          "http://localhost:8000"
      ],
      "realm_access": {
          "roles": [
              "offline_access",
              "default-roles-prp",
              "uma_authorization"
          ]
      },
      "resource_access": {
          "account": {
              "roles": [
                  "manage-account",
                  "manage-account-links",
                  "view-profile"
              ]
          }
      },
      "scope": "openid email profile",
      "email_verified": false,
      "name": "Foo Bar",
      "preferred_username": "foo",
      "given_name": "Foo",
      "family_name": "Bar",
      "email": "foo@bar.com"
  }
  ```

- Visit http://localhost:8080/admin/master/console/#/prp/users and see that we have a new user in Keycloak

- Click on the user `foo` -> `Role mapping` -> `Assign role` -> `Filter by realm roles` -> `PRP-Admin` -> `Assign`

- Do again http://localhost:8000/ -> `Login` -> `Login with Authentik` -> `user123 / userpassword` and see
  ```
  "realm_access": {
        "roles": [
            "PRP-Admin",
            "offline_access",
            "default-roles-prp",
            "uma_authorization"
        ]
    },
  ``` 