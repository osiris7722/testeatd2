# Integração Firebase - Guia de Configuração

## O que foi feito

✓ **Firebase + SQLite Integrado**: A aplicação agora guarda dados em ambos os lugares:
  - **SQLite**: Armazenamento local rápido e confiável
  - **Firebase Firestore**: Sincronização em tempo real e backup na nuvem

## Configuração

### 1. Credenciais Firebase
O ficheiro de credenciais está localizado na raiz do projeto:
```
studio-7634777517-713ea-firebase-adminsdk-fbsvc-7669723ac0.json
```

Este ficheiro contém as chaves de autenticação necessárias.

### 2. Instalação das Dependências
As dependências foram adicionadas ao `requirements.txt`:
```bash
python3 -m pip install -r requirements.txt
```

Pacotes instalados:
- `firebase-admin==6.2.0` - SDK oficial do Firebase para Python

### 3. Estrutura de Dados no Firebase

Os dados são armazenados em **Firestore** com a seguinte estrutura:

```
Firestore
└── feedback/
    ├── feedback_1/
    │   ├── id: 1
    │   ├── grau_satisfacao: "muito_satisfeito"
    │   ├── data: "2026-02-05"
    │   ├── hora: "14:30:00"
    │   ├── dia_semana: "Quinta-feira"
    │   └── timestamp: "2026-02-05T14:30:00.123456"
    ├── feedback_2/
    │   └── ...
```

## Como Funciona

### Fluxo de Dados

1. **Utilizador submete feedback** → API `/api/feedback`
2. **Dados guardados no SQLite** → Armazenamento local imediato
3. **Dados enviados para Firebase** → Sincronização na nuvem
4. **Se Firebase falhar** → Aplicação continua a funcionar normalmente com SQLite

### Código-chave

**app.py** - Inicialização do Firebase:
```python
firebase_db = None
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate('studio-7634777517-713ea-firebase-adminsdk-fbsvc-7669723ac0.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://studio-7634777517-713ea.firebaseio.com'
        })
        firebase_db = firestore.client()
except Exception as e:
    print(f"⚠ Firebase não está disponível: {e}")
```

**Guardar dados em ambos os lugares**:
```python
# SQLite
conn = get_db()
cursor = conn.execute(
    'INSERT INTO feedback (grau_satisfacao, data, hora, dia_semana) VALUES (?, ?, ?, ?)',
    (grau_satisfacao, data_str, hora_str, dia_semana)
)
feedback_id = cursor.lastrowid

# Firebase
if firebase_db:
    firebase_db.collection('feedback').document(f'feedback_{feedback_id}').set(feedback_data)
```

## Variáveis de Ambiente (Opcional)

Para produção, recomenda-se usar variáveis de ambiente:

```bash
export SECRET_KEY="sua_chave_secreta_segura"
export ADMIN_PASSWORD="senha_admin_segura"
export FLASK_ENV="production"
```

## Firebase Web (Admin Login via Authentication)

O login do admin foi migrado para **Firebase Authentication (email + senha)** no browser e o backend valida o **ID Token** (endpoint `POST /api/admin/login/firebase`).

### 1) Ativar Email/Password no Firebase

No Firebase Console:

- **Authentication → Sign-in method → Email/Password → Enable**

Depois cria (ou garante que existe) um utilizador em:

- **Authentication → Users → Add user**

### 2) Configurar o Firebase Web config por variáveis de ambiente

O frontend do login lê a config via `FIREBASE_*` (não usa o ficheiro JSON do Admin SDK). No macOS/zsh podes exportar assim:

```bash
export FIREBASE_API_KEY="AIzaSyAEvUvbhv2vXj8qa1G6r9S8HSr2cFUv_bM"
export FIREBASE_AUTH_DOMAIN="studio-7634777517-713ea.firebaseapp.com"
export FIREBASE_PROJECT_ID="studio-7634777517-713ea"
export FIREBASE_STORAGE_BUCKET="studio-7634777517-713ea.firebasestorage.app"
export FIREBASE_MESSAGING_SENDER_ID="142898689875"
export FIREBASE_APP_ID="1:142898689875:web:726d61b0a2590e7e4c93a6"
export FIREBASE_MEASUREMENT_ID="G-3JZQJD550E"
```

Notas:

- A `apiKey` do Firebase Web **não é segredo** (é identificador do projeto), mas **as regras de acesso** devem ser protegidas via Auth/Regras do Firebase.
- Para o login funcionar, o mínimo costuma ser `FIREBASE_API_KEY`, `FIREBASE_AUTH_DOMAIN`, `FIREBASE_PROJECT_ID`, `FIREBASE_APP_ID`.

### 3) (Recomendado) Restringir quem pode ser admin

No backend podes restringir quem entra no dashboard com:

```bash
export ADMIN_EMAILS="admin1@exemplo.com,admin2@exemplo.com"
# ou
export ADMIN_EMAIL_DOMAIN="exemplo.com"
```

## Verifying Firebase Connection

Para verificar se Firebase está funcionando:

1. Aceda ao [Firebase Console](https://console.firebase.google.com/)
2. Selecione o projeto: **studio-7634777517-713ea**
3. Vá para **Firestore Database**
4. Procure pela coleção **feedback**
5. Veja os documentos que estão sendo criados em tempo real

## Troubleshooting

### Firebase não inicializa?
- ✓ Verificar se o ficheiro JSON está na pasta correta
- ✓ Verificar as permissões do ficheiro
- ✓ Testar a ligação à internet
- ✓ Consultar logs da aplicação

### Dados não aparecem no Firebase?
- ✓ Verificar se `firebase_db` é `None`
- ✓ Consultar as regras de segurança do Firestore
- ✓ Verificar se as credenciais têm permissões de escrita

### Aplicação está lenta?
- ✓ SQLite continua a funcionar normalmente
- ✓ Firebase roda em thread separada (não bloqueia)
- ✓ Considerar cache ou índices no Firestore

## Próximas Etapas

1. **Configurar regras de segurança** no Firestore
2. **Criar índices** para queries mais rápidas
3. **Implementar backup automático** do SQLite
4. **Sincronizar dados históricos** do SQLite para Firebase

## Ficheiros Modificados

- `requirements.txt` - Adicionado firebase-admin
- `app.py` - Integração Firebase + tratamento de erros
- `config.py` - Novo ficheiro com configurações (optional)

---

**Nota**: A aplicação funciona mesmo se Firebase estiver indisponível. Todos os dados são sempre guardados no SQLite.
