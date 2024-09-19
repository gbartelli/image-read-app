# Manual de Uso do Extrator de Texto de Imagens

## Pré-requisitos

Antes de começar, certifique-se de que possui:

1. **Conta no Microsoft Azure**: Você precisará de uma conta ativa para acessar os serviços cognitivos.
2. **Chaves de API do Azure**:
   - **Subscription Key**: A chave de assinatura do serviço de Visão Computacional.
   - **Endpoint**: O endpoint do serviço (URL base).

## Passos para Utilização

### 1. Inicie o Aplicativo

- Localize o arquivo executável do programa (por exemplo, `ExtratorDeTexto.exe`) e dê um duplo clique para executá-lo.

### 2. Insira Suas Credenciais do Azure

- **Subscription Key**:
  - No campo indicado, insira sua Subscription Key do serviço de Visão Computacional.
  - *Nota*: Os caracteres digitados serão ocultados para segurança.
- **Endpoint**:
  - No campo ao lado, insira o Endpoint do serviço. Geralmente tem o formato `https://seu-endpoint.cognitiveservices.azure.com/`.

### 3. Carregue a Imagem

Você tem duas opções para selecionar a imagem da qual deseja extrair o texto:

#### a) Carregar Imagem Local

- Clique no botão **"Carregar imagem local"**.
- Navegue até a pasta onde a imagem está armazenada.
- Selecione a imagem desejada e clique em **"Abrir"**.
- A imagem selecionada será exibida na área destinada no aplicativo.

#### b) Inserir URL da Imagem

- No campo **"Insira o URL da imagem aqui"**, cole o link direto da imagem hospedada na internet.
- *Nota*: Certifique-se de que o URL leva diretamente a um arquivo de imagem (formatos suportados: `.png`, `.jpg`, `.jpeg`, `.bmp`).

### 4. Extrair o Texto

- Após carregar a imagem (local ou via URL) e inserir suas credenciais, clique no botão **"Retirar texto da imagem"**.
- O aplicativo irá processar a imagem utilizando o serviço do Azure.
- Aguarde alguns instantes enquanto o texto é extraído.

### 5. Visualizar o Texto Extraído

- O texto extraído será exibido na caixa de texto na parte inferior do aplicativo.
- Você pode selecionar, copiar e colar esse texto conforme necessário.
