
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer

class TextProcessor:
    exemplos_manual = [
        {"content": "Novas multas foram aplicadas contra empresas envolvidas em desmatamento ilegal na região amazônica.", "classification": "ruim"},
        {"content": "Alertas de desmatamento na Amazônia aumentaram nos últimos meses, exigindo ação imediata das autoridades.", "classification": "ruim"},
        {"content": "O setor da agricultura está pressionando por mais terras, levando ao aumento do desmatamento na região.", "classification": "ruim"},
        {"content": "A agropecuária está contribuindo significativamente para o desmatamento, especialmente na região central do país.", "classification": "ruim"},
        {"content": "As atividades de garimpo ilegal estão devastando as florestas nativas, causando danos irreparáveis ao meio ambiente.", "classification": "ruim"},
        {"content": "Fiscalização mais rigorosa é necessária para conter o desmatamento desenfreado em áreas protegidas.", "classification": "ruim"},
        {"content": "O governo anunciou novas medidas para combater o desmatamento ilegal e proteger as áreas de conservação.", "classification": "boa"},
        {"content": "Estatísticas recentes mostram um aumento alarmante na taxa de desmatamento, destacando a urgência de ações efetivas.", "classification": "ruim"},
        {"content": "Campanhas de conscientização estão sendo lançadas para alertar o público sobre os impactos devastadores do desmatamento.", "classification": "boa"},
        {"content": "Novos dados revelam uma redução significativa no desmatamento em áreas sob monitoramento intensivo.", "classification": "boa"},
        {"content": "A conscientização pública sobre os efeitos negativos do desmatamento está crescendo, impulsionando ações coletivas para proteger as florestas.", "classification": "boa"},
        {"content": "Especialistas afirmam que a redução do desmatamento é crucial para combater as mudanças climáticas e preservar a biodiversidade.", "classification": "boa"},
        {"content": "O desmatamento ilegal continua sendo uma ameaça séria para a sustentabilidade ambiental, exigindo medidas urgentes por parte das autoridades.", "classification": "ruim"},
        {"content": "Agricultores estão sendo incentivados a adotar práticas sustentáveis para evitar o desmatamento e proteger o meio ambiente.", "classification": "boa"},
        {"content": "O aumento do desmatamento está relacionado principalmente à expansão descontrolada da fronteira agrícola.", "classification": "ruim"},
        {"content": "A criminalidade ambiental está em alta, com o desmatamento ilegal sendo uma das principais preocupações das autoridades.", "classification": "ruim"},
        {"content": "Especialistas alertam que o desmatamento está colocando em risco a sobrevivência de várias espécies de animais e plantas.", "classification": "ruim"},
        {"content": "O desmatamento está afetando negativamente as comunidades locais, prejudicando seu sustento e qualidade de vida.", "classification": "ruim"},
        {"content": "A falta de fiscalização adequada está permitindo o avanço do desmatamento em áreas protegidas.", "classification": "ruim"},
        {"content": "O desmatamento ilegal está causando erosão do solo e degradação do ecossistema, ameaçando a saúde dos rios e riachos locais.", "classification": "ruim"},
        {"content": "Os esforços para conter o desmatamento precisam ser intensificados, envolvendo uma colaboração efetiva entre governo, empresas e comunidades locais.", "classification": "boa"},
        {"content": "A expansão da agricultura e pecuária está contribuindo significativamente para o aumento do desmatamento em áreas sensíveis.", "classification": "ruim"},
        {"content": "O desmatamento descontrolado está levando à perda de habitats naturais e à fragmentação de ecossistemas.", "classification": "ruim"},
        {"content": "A sociedade civil está pressionando por ações mais enérgicas contra o desmatamento ilegal e a destruição de florestas.", "classification": "boa"},
        {"content": "O desmatamento está comprometendo a capacidade das florestas de atuar como sumidouros de carbono, exacerbando as mudanças climáticas.", "classification": "ruim"},
        {"content": "Autoridades estão investigando denúncias de desmatamento ilegal em uma área de conservação protegida.", "classification": "ruim"},
        {"content": "A recuperação de áreas desmatadas requer investimentos significativos em reflorestamento e restauração ecológica.", "classification": "boa"},
        {"content": "O desmatamento está contribuindo para o aumento da temperatura global, afetando diretamente o clima e os padrões de precipitação.", "classification": "ruim"},
        {"content": "A perda de cobertura florestal está diminuindo a resiliência dos ecossistemas, tornando-os mais vulneráveis ​​a incêndios e secas.", "classification": "ruim"},
        {"content": "O desmatamento ilegal está alimentando o ciclo de degradação ambiental, prejudicando a saúde do planeta e das futuras gerações.", "classification": "ruim"},
        {"content": "A destruição de habitats naturais está empurrando várias espécies à beira da extinção, ameaçando a biodiversidade global.", "classification": "ruim"},
        {"content": "O desmatamento está contribuindo para o aumento da pressão sobre as populações indígenas e tradicionais, prejudicando seus meios de subsistência e cultura.", "classification": "ruim"},
        {"content": "A crescente demanda por commodities agrícolas está impulsionando o desmatamento em regiões de alto valor ecológico.", "classification": "ruim"},
        {"content": "O desmatamento está prejudicando os serviços ecossistêmicos essenciais, como a regulação do clima e o fornecimento de água limpa.", "classification": "ruim"},
        {"content": "A redução do desmatamento é fundamental para alcançar os objetivos de desenvolvimento sustentável e promover uma coexistência harmoniosa entre humanos e natureza.", "classification": "boa"},
        {"content": "O desmatamento está exacerbando os efeitos das mudanças climáticas, aumentando a frequência e intensidade de eventos climáticos extremos.", "classification": "ruim"},
        {"content": "A perda de florestas está privando as comunidades locais de recursos naturais vitais, como alimentos, medicamentos e materiais de construção.", "classification": "ruim"},
        {"content": "A conservação das florestas é essencial para garantir a segurança hídrica e a estabilidade climática em escala regional e global.", "classification": "boa"},
        {"content": "O desmatamento está contribuindo para a destruição de habitats críticos para a reprodução e migração de espécies migratórias.", "classification": "ruim"},
        {"content": "A exploração madeireira ilegal está desencadeando um ciclo de degradação ambiental, comprometendo a saúde dos ecossistemas florestais.", "classification": "ruim"},
        {"content": "O desmatamento está colocando em risco a segurança alimentar e a subsistência de milhões de pessoas que dependem das florestas para sua sobrevivência.", "classification": "ruim"},
        {"content": "A destruição de florestas está privando o mundo de potenciais fontes de medicamentos e produtos naturais de alto valor.", "classification": "ruim"},
        {"content": "O desmatamento está desencadeando um ciclo de degradação ambiental que ameaça a estabilidade ecológica e socioeconômica de vastas regiões.", "classification": "ruim"},
        {"content": "A implementação de políticas eficazes é crucial para conter o desmatamento e promover o manejo sustentável das florestas.", "classification": "boa"},
        {"content": "O desmatamento está prejudicando a capacidade das florestas de absorver carbono, contribuindo diretamente para o aumento das concentrações de CO2 na atmosfera.", "classification": "ruim"},
        {"content": "A restauração de paisagens degradadas é fundamental para reverter os danos causados ​​pelo desmatamento e promover a recuperação dos ecossistemas.", "classification": "boa"},
        {"content": "O desmatamento está minando os esforços globais para combater a perda de biodiversidade e preservar as espécies ameaçadas.", "classification": "ruim"},
        {"content": "A destruição de florestas está contribuindo para a fragmentação de habitats, isolando populações de animais e reduzindo sua capacidade de sobreviver e se reproduzir.", "classification": "ruim"},
        {"content": "O desmatamento está exacerbando os impactos das mudanças climáticas em comunidades vulneráveis, aumentando a frequência e intensidade de eventos climáticos extremos.", "classification": "ruim"},
        {"content": "A perda de florestas está reduzindo a resiliência dos ecossistemas, tornando-os mais suscetíveis a doenças e invasões de espécies exóticas.", "classification": "ruim"},
        {"content": "A degradação de florestas está comprometendo a capacidade dos ecossistemas de fornecer serviços essenciais, como a purificação do ar e da água.", "classification": "ruim"},
        {"content": "O desmatamento está privando as comunidades locais de suas conexões culturais e espirituais com a terra, causando danos psicológicos e emocionais.", "classification": "ruim"},
        {"content": "A perda de florestas está contribuindo para a diminuição da diversidade genética das espécies, reduzindo sua capacidade de se adaptar a mudanças ambientais.", "classification": "ruim"},
        {"content": "O desmatamento está comprometendo a integridade dos ecossistemas costeiros e marinhos, afetando negativamente a saúde dos oceanos e a biodiversidade marinha.", "classification": "ruim"},
        {"content": "A destruição de florestas está prejudicando os meios de subsistência de comunidades locais que dependem da pesca e da coleta de recursos naturais para sua sobrevivência.", "classification": "ruim"},
        {"content": "Um aumento nas multas por desmatamento ilegal foi registrado no último trimestre.", "classification": "ruim"},
        {"content": "Alertas recentes indicam um aumento alarmante no desmatamento na região costeira.", "classification": "ruim"},
        {"content": "A agricultura intensiva está contribuindo para a degradação acelerada das florestas tropicais.", "classification": "ruim"},
        {"content": "A agropecuária irresponsável está resultando em extensas áreas desmatadas em todo o país.", "classification": "ruim"},
        {"content": "Empresas de garimpo ilegal estão devastando áreas protegidas em busca de recursos minerais.", "classification": "ruim"},
        {"content": "A falta de fiscalização está permitindo o desmatamento ilegal ocorrer sem punição.", "classification": "ruim"},
        {"content": "O governo anunciou uma nova ação governamental para conter o desmatamento na Amazônia.", "classification": "boa"},
        {"content": "As estatísticas mais recentes mostram uma queda significativa no desmatamento em algumas regiões.", "classification": "boa"},
        {"content": "Campanhas de conscientização estão sendo lançadas para educar o público sobre os impactos do desmatamento.", "classification": "boa"},
        {"content": "Novos dados revelam uma redução na taxa de desmatamento em comparação com o ano passado.", "classification": "boa"},
        {"content": "A conscientização pública sobre a importância das florestas está aumentando.", "classification": "boa"},
        {"content": "Especialistas em conservação estão elogiando os esforços recentes para proteger as áreas florestais.", "classification": "boa"},
        {"content": "O desmatamento está diminuindo a capacidade das florestas de regular o clima global.", "classification": "ruim"},
        {"content": "A conscientização sobre a conservação das florestas está crescendo entre os jovens.", "classification": "boa"},
        {"content": "A agricultura sustentável está sendo promovida como uma alternativa ao desmatamento.", "classification": "boa"},
        {"content": "O desmatamento está ameaçando a sobrevivência de espécies em perigo de extinção.", "classification": "ruim"},
        {"content": "A perda de florestas está contribuindo para a erosão do solo em áreas rurais.", "classification": "ruim"},
        {"content": "O desmatamento ilegal está alimentando o comércio ilegal de madeira.", "classification": "ruim"},
        {"content": "As comunidades indígenas estão lutando para proteger suas terras ancestrais do desmatamento.", "classification": "boa"},
        {"content": "O desmatamento está resultando em perdas econômicas significativas para os países afetados.", "classification": "ruim"},
        {"content": "A falta de regulamentação está permitindo que empresas explorem florestas sem restrições.", "classification": "ruim"},
        {"content": "O governo está investindo em tecnologias de monitoramento para detectar desmatamento ilegal mais rapidamente.", "classification": "boa"},
        {"content": "A conscientização sobre os benefícios das florestas está levando a um aumento no ativismo ambiental.", "classification": "boa"},
        {"content": "O desmatamento está prejudicando a capacidade das florestas de absorver carbono da atmosfera.", "classification": "ruim"},
        {"content": "A redução do desmatamento é essencial para alcançar as metas de mitigação das mudanças climáticas.", "classification": "boa"},
        {"content": "O desmatamento está causando um declínio na diversidade genética das florestas.", "classification": "ruim"},
        {"content": "As autoridades estão enfrentando resistência ao tentar conter o desmatamento ilegal.", "classification": "ruim"},
        {"content": "O desmatamento está destruindo habitats essenciais para a vida selvagem.", "classification": "ruim"},
        {"content": "A expansão urbana está contribuindo para o desmatamento em áreas metropolitanas.", "classification": "ruim"},
        {"content": "O desmatamento está aumentando a vulnerabilidade das comunidades locais a desastres naturais.", "classification": "ruim"},
        {"content": "A degradação florestal está reduzindo a capacidade das florestas de fornecer água limpa.", "classification": "ruim"},
        {"content": "O desmatamento está resultando em perdas econômicas para as indústrias que dependem de produtos florestais.", "classification": "ruim"},
        {"content": "A recuperação de áreas desmatadas é uma prioridade para restaurar a biodiversidade perdida.", "classification": "boa"},
        {"content": "O desmatamento está aumentando a incidência de conflitos entre comunidades locais e empresas madeireiras.", "classification": "ruim"},
        {"content": "A expansão das fronteiras agrícolas está levando à destruição de florestas em todo o mundo.", "classification": "ruim"},
        {"content": "O desmatamento está prejudicando os meios de subsistência das populações locais que dependem da floresta para sua sobrevivência.", "classification": "ruim"},
        {"content": "A perda de florestas está comprometendo a capacidade das regiões de mitigar os efeitos das mudanças climáticas.", "classification": "ruim"},
        {"content": "O desmatamento está diminuindo a resiliência dos ecossistemas florestais a incêndios e secas.", "classification": "ruim"},
        {"content": "A perda de biodiversidade causada pelo desmatamento está diminuindo a capacidade das florestas de se regenerar naturalmente.", "classification": "ruim"},
        {"content": "O desmatamento está afetando negativamente a saúde mental das comunidades que dependem da floresta para sua subsistência.", "classification": "ruim"},
        {"content": "A urbanização desenfreada está contribuindo para o desmatamento em áreas próximas a grandes cidades.", "classification": "ruim"},
        {"content": "O desmatamento está privando as comunidades locais de recursos naturais essenciais, como lenha e água potável.", "classification": "ruim"},
        {"content": "A perda de florestas está diminuindo a capacidade das regiões de se adaptar às mudanças climáticas.", "classification": "ruim"},
        {"content": "O desmatamento está degradando os ecossistemas costeiros, ameaçando a vida marinha.", "classification": "ruim"},
        {"content": "A falta de educação ambiental está contribuindo para a perpetuação do desmatamento.", "classification": "ruim"},
        {"content": "O desmatamento está prejudicando a capacidade das florestas de regular o ciclo da água.", "classification": "ruim"},
        {"content": "A perda de florestas está privando as comunidades locais de oportunidades de ecoturismo e recreação.", "classification": "ruim"},
        {"content": "O desmatamento está causando perdas econômicas significativas para os setores de pesca e turismo.", "classification": "ruim"},
        {"content": "A recuperação de áreas desmatadas é essencial para restaurar a biodiversidade e os serviços ecossistêmicos.", "classification": "boa"},
        {"content": "O desmatamento está comprometendo a capacidade das florestas de atuar como barreiras naturais contra deslizamentos de terra e inundações.", "classification": "ruim"},
        {"content": "A expansão das fronteiras agrícolas está levando à perda de habitats críticos para a vida selvagem.", "classification": "ruim"},
        {"content": "O desmatamento está diminuindo a capacidade das florestas de servir como refúgio para espécies ameaçadas.", "classification": "ruim"},
        {"content": "A fragmentação de habitats causada pelo desmatamento está aumentando a vulnerabilidade das populações de animais selvagens.", "classification": "ruim"},
        {"content": "O desmatamento está exacerbando a escassez de água em áreas propensas à seca.", "classification": "ruim"},
        {"content": "A perda de florestas está diminuindo a capacidade das regiões de filtrar poluentes do ar e da água.", "classification": "ruim"},
        {"content": "O desmatamento está prejudicando a capacidade das florestas de fornecer habitats para espécies migratórias.", "classification": "ruim"},
        {"content": "A urbanização está contribuindo para a destruição de florestas em áreas urbanas e periurbanas.", "classification": "ruim"},
        {"content": "O desmatamento está aumentando a frequência e intensidade de conflitos entre comunidades locais e empresas madeireiras.", "classification": "ruim"},
        {"content": "A expansão das atividades agrícolas está levando à destruição de florestas em todo o mundo.", "classification": "ruim"},
        {"content": "O desmatamento está comprometendo os serviços ecossistêmicos essenciais fornecidos pelas florestas.", "classification": "ruim"},
        {"content": "A perda de florestas está afetando negativamente a saúde física e mental das comunidades locais.", "classification": "ruim"},
        {"content": "O desmatamento está prejudicando a capacidade das florestas de absorver CO2 da atmosfera.", "classification": "ruim"},
        {"content": "A urbanização descontrolada está contribuindo para a destruição de florestas em áreas urbanas e periurbanas.", "classification": "ruim"},
        {"content": "O desmatamento está exacerbando a escassez de alimentos em áreas rurais afetadas.", "classification": "ruim"},
        {"content": "A perda de florestas está diminuindo a capacidade das regiões de regular o clima global.", "classification": "ruim"},
        {"content": "O desmatamento está comprometendo a capacidade das florestas de fornecer habitats para a vida selvagem.", "classification": "ruim"},
        {"content": "A urbanização rápida está levando à destruição de florestas em áreas metropolitanas.", "classification": "ruim"},
        {"content": "O desmatamento está aumentando a incidência de doenças transmitidas por vetores em áreas desmatadas.", "classification": "ruim"},
        {"content": "A perda de florestas está aumentando a vulnerabilidade das populações locais a desastres naturais.", "classification": "ruim"},
        {"content": "O desmatamento está prejudicando a capacidade das florestas de regular o ciclo da água.", "classification": "ruim"},
        {"content": "A urbanização desenfreada está contribuindo para a perda de habitats críticos para a vida selvagem.", "classification": "ruim"},
        {"content": "O desmatamento está exacerbando a erosão do solo em áreas rurais afetadas.", "classification": "ruim"},
        {"content": "A perda de florestas está comprometendo a capacidade das regiões de fornecer serviços ecossistêmicos essenciais.", "classification": "ruim"},
        {"content": "O desmatamento está diminuindo a capacidade das florestas de fornecer refúgio para espécies ameaçadas.", "classification": "ruim"},
        {"content": "A urbanização descontrolada está contribuindo para a destruição de habitats críticos para a vida selvagem.", "classification": "ruim"},
        {"content": "O desmatamento está aumentando a exposição das comunidades locais a desastres naturais.", "classification": "ruim"},
        {"content": "A perda de florestas está prejudicando a capacidade das regiões de fornecer abrigo para espécies migratórias.", "classification": "ruim"},
        {"content": "O desmatamento está exacerbando a escassez de água em áreas urbanas afetadas.", "classification": "ruim"},
        {"content": "A urbanização rápida está contribuindo para a perda de habitats críticos para a biodiversidade.", "classification": "ruim"},
        {"content": "O desmatamento está aumentando a incidência de conflitos entre comunidades locais e empresas madeireiras.", "classification": "ruim"},
        {"content": "A perda de florestas está prejudicando a capacidade das regiões de regular o clima local.", "classification": "ruim"},
        {"content": "O desmatamento está comprometendo a capacidade das florestas de fornecer abrigo para espécies ameaçadas.", "classification": "ruim"},
        {"content": "A taxa de desmatamento na Amazônia caiu para o nível mais baixo em uma década.", "classification": "boa"},
        {"content": "Uma queda significativa no desmatamento foi observada em áreas protegidas nos últimos anos.","classification": "boa"},
        { "content": "Os esforços de conservação resultaram em uma redução de 30% no desmatamento em comparação com o ano passado.","classification": "boa"},
        {"content": "A implementação de medidas de proteção levou a uma redução de 50% na taxa de desmatamento em regiões críticas.","classification": "boa"},
        {"content": "Novos dados revelam uma queda de 25% no desmatamento em florestas tropicais em todo o mundo.","classification": "boa"},
        {"content": "As políticas de uso sustentável da terra estão mostrando resultados positivos, com uma redução notável no desmatamento.","classification": "boa"},
        {"content": "A conscientização pública sobre a importância das florestas resultou em uma queda acentuada no desmatamento em áreas sensíveis.","classification": "boa"},
        {"content": "A adoção de práticas agrícolas sustentáveis está contribuindo para a redução do desmatamento em regiões agrícolas.","classification": "boa"},
        {"content": "Programas de reflorestamento estão ajudando a restaurar áreas desmatadas, contribuindo para a redução do desmatamento líquido.","classification": "boa"},
        {"content": "As parcerias entre governos, ONGs e comunidades locais estão resultando em uma queda gradual e sustentada no desmatamento.","classification": "boa"},
        {"content": "A introdução de incentivos financeiros para conservação está incentivando os proprietários de terras a proteger as florestas, levando a uma redução no desmatamento.","classification": "boa"},
        {"content": "Os esforços para promover o manejo sustentável das florestas estão levando a uma queda constante na taxa de desmatamento em todo o mundo.","classification": "boa"},
        {"content": "A implementação de políticas de conservação mais rigorosas resultou em uma redução notável no desmatamento ilegal.","classification": "boa"},
        {"content": "A conscientização sobre os benefícios econômicos das florestas está levando a uma redução do desmatamento em áreas economicamente vulneráveis.","classification": "boa"},
        {"content": "A queda na demanda por produtos de madeira ilegais está contribuindo para a redução do desmatamento em florestas primárias.","classification": "boa"},
        {"content": "A conscientização sobre os impactos do desmatamento na biodiversidade está resultando em uma queda na conversão de habitats naturais.","classification": "boa"},
        {"content": "As comunidades locais estão liderando esforços de conservação que estão resultando em uma queda acentuada no desmatamento em suas áreas.","classification": "boa"},
        {"content": "O aumento do ecoempreendedorismo está impulsionando a economia local e contribuindo para a redução do desmatamento.", "classification": "boa"},
        {"content": "A adoção de tecnologias de monitoramento remoto está permitindo uma resposta mais rápida ao desmatamento, levando a uma redução da área desmatada.","classification": "boa"},
        { "content": "O aumento do investimento em pesquisa de conservação está gerando novas estratégias eficazes para reduzir o desmatamento.","classification": "boa"},
        {"content": "Investimentos em pesquisa de ponta estão revelando soluções inovadoras para reduzir o desmatamento de forma eficaz.","classification": "boa"},
        {"content": "Programas de educação ambiental estão capacitando comunidades locais a se tornarem defensores ativos da preservação florestal.","classification": "boa"},
        {"content": "Parcerias público-privadas estão impulsionando iniciativas sustentáveis que promovem o reflorestamento e a conservação de habitats naturais.","classification": "boa"},
        { "content": "Avanços tecnológicos estão aprimorando os sistemas de monitoramento, permitindo uma detecção precoce e resposta rápida ao desmatamento.","classification": "boa"},
        {"content": "Estratégias de restauração ecológica estão recuperando áreas degradadas, restaurando a biodiversidade e os serviços ecossistêmicos.","classification": "boa"},
        {"content": "A conscientização global está gerando um movimento crescente em direção à preservação ambiental e à redução do desmatamento.","classification": "boa"},
        {"content": "Iniciativas de pagamento por serviços ambientais estão incentivando proprietários de terras a conservar florestas e ecossistemas valiosos.","classification": "boa"},
        {"content": "Políticas de conservação eficazes estão sendo implementadas em nível nacional e internacional para proteger as florestas do mundo.","classification": "boa"},
        {"content": "Comunidades indígenas estão liderando esforços de conservação que promovem a gestão sustentável das florestas e o respeito pelos conhecimentos tradicionais.","classification": "boa"},
        { "content": "A conscientização sobre a importância das florestas está motivando indivíduos e organizações a adotarem práticas de consumo responsável e sustentável.","classification": "boa"},
        {"content": "A implementação de políticas de reflorestamento está restaurando ecossistemas florestais degradados e criando oportunidades econômicas para comunidades locais.","classification": "boa"},
        {"content": "Estratégias de conservação baseadas na comunidade estão fortalecendo os laços sociais e promovendo o desenvolvimento sustentável em áreas rurais.","classification": "boa"},
        {"content": "A expansão de áreas protegidas e reservas naturais está garantindo a preservação de habitats críticos e ecossistemas únicos em todo o mundo.","classification": "boa"},
        { "content": "A promoção de práticas agrícolas sustentáveis está ajudando a reduzir a pressão sobre as florestas, ao mesmo tempo em que melhora a produtividade e a resiliência das terras cultivadas.","classification": "boa"},
        { "content": "A conscientização sobre os impactos socioambientais do desmatamento está promovendo mudanças positivas no comportamento e nas políticas em todos os níveis da sociedade.","classification": "boa"},
        {"content": "A colaboração entre setores público e privado está impulsionando iniciativas inovadoras de restauração florestal e conservação de biodiversidade em todo o mundo.","classification": "boa"},
        { "content": "A integração de estratégias de conservação e desenvolvimento está promovendo o crescimento econômico sustentável e a proteção ambiental em regiões rurais e urbanas.","classification": "boa"},
        {"content": "O engajamento da juventude está catalisando movimentos ambientais globais e promovendo uma cultura de sustentabilidade e responsabilidade ambiental.","classification": "boa"},
        {"content": "A restauração de ecossistemas degradados está criando novas oportunidades de emprego e empreendedorismo, ao mesmo tempo em que fortalece a resiliência ambiental das comunidades locais.","classification": "boa"},
        {"content": "A implementação de práticas de manejo florestal sustentável está garantindo a conservação de florestas nativas e a geração de renda para as comunidades que dependem delas.","classification": "boa"},
        {"content": "A transição para fontes de energia renovável está reduzindo a dependência de recursos naturais não renováveis, ajudando a mitigar o desmatamento e as emissões de gases de efeito estufa.","classification": "boa"},
        {"content": "O reconhecimento dos direitos das comunidades locais sobre suas terras tradicionais está fortalecendo a gestão sustentável dos recursos naturais e a conservação das florestas.","classification": "boa"},
        {"content": "A conscientização sobre a importância da biodiversidade está incentivando a proteção de habitats críticos e a preservação de espécies ameaçadas em todo o mundo.","classification": "boa"},
        {"content": "A adoção de tecnologias limpas e práticas de produção sustentável está promovendo a conservação de recursos naturais e a redução da pegada ambiental das atividades humanas.","classification": "boa"}
    ]

    def __init__(self):
        self.df = pd.DataFrame(TextProcessor.exemplos_manual)

        # Baixar stopwords para o idioma português
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('portuguese'))

        # Criar o stemmer para o português
        self.stemmer = RSLPStemmer()

    def preprocess_text(self, text):
        tokens = nltk.word_tokenize(text.lower())  # Tokenização e conversão para minúsculas
        stemmed_tokens = [self.stemmer.stem(word) for word in tokens if
                          word not in self.stop_words]  # Stemming e remoção de stopwords
        return ' '.join(stemmed_tokens)

    def process_texts(self):
        # Aplicar a função de pré-processamento em todas as frases do DataFrame
        self.df['processed_content'] = self.df['content'].apply(self.preprocess_text)

    def save_to_excel(self, filename):
        # Salvando o DataFrame com as frases processadas em um arquivo Excel
        self.df.to_excel(filename, index=False)


if __name__ == "__main__":
    text_processor = TextProcessor()
    text_processor.process_texts()
    text_processor.save_to_excel('treino.xlsx')
