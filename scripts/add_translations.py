#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para adicionar traduções aos arquivos .po
"""

# Dicionário completo de traduções PT -> EN -> FR
translations = {
    # Hero Section
    "Transforme Momentos Especiais": {
        "en": "Transform Special Moments",
        "fr": "Transformez les Moments Spéciaux"
    },
    "em Memórias Deliciosas": {
        "en": "into Delicious Memories",
        "fr": "en Souvenirs Délicieux"
    },
    "Bolos artesanais personalizados, feitos com amor e dedicação para o seu evento único": {
        "en": "Handcrafted custom cakes, made with love and dedication for your unique event",
        "fr": "Gâteaux artisanaux personnalisés, faits avec amour et dévouement pour votre événement unique"
    },
    "Ver Portfólio": {
        "en": "View Portfolio",
        "fr": "Voir le Portfolio"
    },
    "Fazer Encomenda": {
        "en": "Place Order",
        "fr": "Passer Commande"
    },
    
    # About Section
    "Sobre Nós": {
        "en": "About Us",
        "fr": "À Propos"
    },
    "A Magia por Trás de Cada Bolo": {
        "en": "The Magic Behind Every Cake",
        "fr": "La Magie Derrière Chaque Gâteau"
    },
    "Anos de Experiência": {
        "en": "Years of Experience",
        "fr": "Années d'Expérience"
    },
    "Olá! Sou a": {
        "en": "Hello! I'm",
        "fr": "Bonjour ! Je suis"
    },
    "e transformar sonhos em bolos é a minha paixão.": {
        "en": "and turning dreams into cakes is my passion.",
        "fr": "et transformer les rêves en gâteaux est ma passion."
    },
    "Cada bolo que crio é uma obra de arte personalizada, pensada ao detalhe para celebrar os seus momentos mais especiais. Desde festas de aniversário infantis repletas de cor e diversão, até celebrações elegantes de marcos importantes da vida.": {
        "en": "Every cake I create is a personalized work of art, thoughtfully designed to celebrate your most special moments. From children's birthday parties full of color and fun, to elegant celebrations of important life milestones.",
        "fr": "Chaque gâteau que je crée est une œuvre d'art personnalisée, conçue avec soin pour célébrer vos moments les plus spéciaux. Des fêtes d'anniversaire pour enfants pleines de couleur et de plaisir, aux célébrations élégantes des étapes importantes de la vie."
    },
    "Com anos de experiência em confeitaria artesanal, combino técnicas tradicionais com criatividade moderna para entregar não apenas um bolo, mas uma experiência memorável.": {
        "en": "With years of experience in artisan confectionery, I combine traditional techniques with modern creativity to deliver not just a cake, but a memorable experience.",
        "fr": "Avec des années d'expérience en pâtisserie artisanale, je combine des techniques traditionnelles avec une créativité moderne pour offrir non seulement un gâteau, mais une expérience mémorable."
    },
    "O seu momento especial merece um bolo igualmente especial. Vamos criar magia juntos?": {
        "en": "Your special moment deserves an equally special cake. Let's create magic together?",
        "fr": "Votre moment spécial mérite un gâteau tout aussi spécial. Créons de la magie ensemble ?"
    },
    "Bolos Criados": {
        "en": "Cakes Created",
        "fr": "Gâteaux Créés"
    },
    "Clientes Felizes": {
        "en": "Happy Clients",
        "fr": "Clients Satisfaits"
    },
    "Feito à Mão": {
        "en": "Handmade",
        "fr": "Fait à la Main"
    },
    
    # Portfolio
    "O Nosso Portfólio": {
        "en": "Our Portfolio",
        "fr": "Notre Portfolio"
    },
    "Cada bolo conta uma história única": {
        "en": "Every cake tells a unique story",
        "fr": "Chaque gâteau raconte une histoire unique"
    },
    "Todos": {
        "en": "All",
        "fr": "Tous"
    },
    "Bolos Infantis": {
        "en": "Children's Cakes",
        "fr": "Gâteaux pour Enfants"
    },
    "Bolos Adultos": {
        "en": "Adult Cakes",
        "fr": "Gâteaux pour Adultes"
    },
    "Bolos Casamento": {
        "en": "Wedding Cakes",
        "fr": "Gâteaux de Mariage"
    },
    "Minimalistas": {
        "en": "Minimalist",
        "fr": "Minimalistes"
    },
    "Temáticos": {
        "en": "Themed",
        "fr": "Thématiques"
    },
    
    # Services
    "Os Nossos Serviços": {
        "en": "Our Services",
        "fr": "Nos Services"
    },
    "Bolos Temáticos Infantis": {
        "en": "Children's Themed Cakes",
        "fr": "Gâteaux Thématiques pour Enfants"
    },
    "Personagens favoritos, cores vibrantes e muita diversão para tornar o aniversário inesquecível": {
        "en": "Favorite characters, vibrant colors and lots of fun to make the birthday unforgettable",
        "fr": "Personnages préférés, couleurs vibrantes et beaucoup de plaisir pour rendre l'anniversaire inoubliable"
    },
    "Stitch, Vampirina, Super-Heróis, Princesas": {
        "en": "Stitch, Vampirina, Superheroes, Princesses",
        "fr": "Stitch, Vampirina, Super-héros, Princesses"
    },
    "Celebrações Elegantes": {
        "en": "Elegant Celebrations",
        "fr": "Célébrations Élégantes"
    },
    "Designs sofisticados para aniversários especiais, bodas e celebrações de marcos importantes": {
        "en": "Sophisticated designs for special birthdays, anniversaries and milestone celebrations",
        "fr": "Designs sophistiqués pour les anniversaires spéciaux, les noces et les célébrations d'étapes importantes"
    },
    "18 anos, 50/60 anos, Bodas, Formaturas": {
        "en": "18th birthday, 50/60 years, Anniversaries, Graduations",
        "fr": "18 ans, 50/60 ans, Noces, Remises de diplômes"
    },
    "Casamentos & Eventos": {
        "en": "Weddings & Events",
        "fr": "Mariages & Événements"
    },
    "Bolos de casamento clássicos e modernos, naked cakes, bolos de noivado": {
        "en": "Classic and modern wedding cakes, naked cakes, engagement cakes",
        "fr": "Gâteaux de mariage classiques et modernes, naked cakes, gâteaux de fiançailles"
    },
    "Naked cakes, Multi-tier, Minimalistas": {
        "en": "Naked cakes, Multi-tier, Minimalist",
        "fr": "Naked cakes, Multi-étages, Minimalistes"
    },
    "Bolos Corporativos": {
        "en": "Corporate Cakes",
        "fr": "Gâteaux d'Entreprise"
    },
    "Eventos empresariais, inaugurações, branding personalizado em pasta de açúcar": {
        "en": "Corporate events, inaugurations, personalized branding in sugar paste",
        "fr": "Événements d'entreprise, inaugurations, branding personnalisé en pâte à sucre"
    },
    "Eventos, Inaugurações, Branding": {
        "en": "Events, Inaugurations, Branding",
        "fr": "Événements, Inaugurations, Branding"
    },
    "Minimalistas & Modernos": {
        "en": "Minimalist & Modern",
        "fr": "Minimalistes & Modernes"
    },
    "Linhas limpas, elegância atemporal, decorações delicadas e sofisticadas": {
        "en": "Clean lines, timeless elegance, delicate and sophisticated decorations",
        "fr": "Lignes épurées, élégance intemporelle, décorations délicates et sophistiquées"
    },
    "Clean design, Elegância, Sutileza": {
        "en": "Clean design, Elegance, Subtlety",
        "fr": "Design épuré, Élégance, Subtilité"
    },
    "Encomendas Personalizadas": {
        "en": "Custom Orders",
        "fr": "Commandes Personnalisées"
    },
    "Tem uma ideia única? Trabalhamos consigo para criar o bolo dos seus sonhos": {
        "en": "Have a unique idea? We work with you to create your dream cake",
        "fr": "Vous avez une idée unique ? Nous travaillons avec vous pour créer le gâteau de vos rêves"
    },
    "Criatividade, Personalização, Sonhos": {
        "en": "Creativity, Customization, Dreams",
        "fr": "Créativité, Personnalisation, Rêves"
    },
    
    # Pricing
    "Investimento": {
        "en": "Investment",
        "fr": "Investissement"
    },
    "Preços transparentes para o seu orçamento": {
        "en": "Transparent prices for your budget",
        "fr": "Prix transparents pour votre budget"
    },
    "Pacote Básico": {
        "en": "Basic Package",
        "fr": "Forfait de Base"
    },
    "Doçura Simples": {
        "en": "Simple Sweetness",
        "fr": "Douceur Simple"
    },
    "A partir de": {
        "en": "Starting from",
        "fr": "À partir de"
    },
    "Bolo redondo 15cm (6-8 pessoas)": {
        "en": "Round cake 15cm (6-8 servings)",
        "fr": "Gâteau rond 15cm (6-8 personnes)"
    },
    "1 sabor à escolha": {
        "en": "1 flavor of choice",
        "fr": "1 parfum au choix"
    },
    "Cobertura buttercream": {
        "en": "Buttercream frosting",
        "fr": "Glaçage buttercream"
    },
    "Decoração simples": {
        "en": "Simple decoration",
        "fr": "Décoration simple"
    },
    "Topper personalizado básico": {
        "en": "Basic custom topper",
        "fr": "Topper personnalisé basique"
    },
    "Entrega na área local": {
        "en": "Local area delivery",
        "fr": "Livraison locale"
    },
    "Escolher Pacote": {
        "en": "Choose Package",
        "fr": "Choisir le Forfait"
    },
    "Pacote Standard": {
        "en": "Standard Package",
        "fr": "Forfait Standard"
    },
    "Momento Especial": {
        "en": "Special Moment",
        "fr": "Moment Spécial"
    },
    "Mais Popular": {
        "en": "Most Popular",
        "fr": "Le Plus Populaire"
    },
    "Bolo redondo 20cm (12-15 pessoas)": {
        "en": "Round cake 20cm (12-15 servings)",
        "fr": "Gâteau rond 20cm (12-15 personnes)"
    },
    "2 sabores à escolha": {
        "en": "2 flavors of choice",
        "fr": "2 parfums au choix"
    },
    "Cobertura premium (fondant/buttercream)": {
        "en": "Premium frosting (fondant/buttercream)",
        "fr": "Glaçage premium (fondant/buttercream)"
    },
    "Decoração personalizada média": {
        "en": "Medium custom decoration",
        "fr": "Décoration personnalisée moyenne"
    },
    "Topper personalizado + flores açúcar": {
        "en": "Custom topper + sugar flowers",
        "fr": "Topper personnalisé + fleurs en sucre"
    },
    "Cores customizadas": {
        "en": "Custom colors",
        "fr": "Couleurs personnalisées"
    },
    "Entrega premium": {
        "en": "Premium delivery",
        "fr": "Livraison premium"
    },
    "Pacote Premium": {
        "en": "Premium Package",
        "fr": "Forfait Premium"
    },
    "Sonho Realizado": {
        "en": "Dream Come True",
        "fr": "Rêve Réalisé"
    },
    "Multi-tier ou tamanho XL (25+ pessoas)": {
        "en": "Multi-tier or XL size (25+ servings)",
        "fr": "Multi-étages ou taille XL (25+ personnes)"
    },
    "3+ sabores à escolha": {
        "en": "3+ flavors of choice",
        "fr": "3+ parfums au choix"
    },
    "Decoração complexa e artística": {
        "en": "Complex and artistic decoration",
        "fr": "Décoration complexe et artistique"
    },
    "Flores naturais/pasta açúcar premium": {
        "en": "Natural flowers/premium sugar paste",
        "fr": "Fleurs naturelles/pâte à sucre premium"
    },
    "Toppers sculpted personalizados": {
        "en": "Custom sculpted toppers",
        "fr": "Toppers sculptés personnalisés"
    },
    "Texturas douradas/prateadas": {
        "en": "Gold/silver textures",
        "fr": "Textures dorées/argentées"
    },
    "Sessão de design detalhada": {
        "en": "Detailed design session",
        "fr": "Session de design détaillée"
    },
    "Entrega e setup incluídos": {
        "en": "Delivery and setup included",
        "fr": "Livraison et installation incluses"
    },
    "*Os preços são indicativos e variam conforme complexidade, tamanho e decoração.<br>Contacte-nos para orçamento personalizado.": {
        "en": "*Prices are indicative and vary according to complexity, size and decoration.<br>Contact us for a custom quote.",
        "fr": "*Les prix sont indicatifs et varient selon la complexité, la taille et la décoration.<br>Contactez-nous pour un devis personnalisé."
    },
    "Pedir Orçamento Gratuito": {
        "en": "Request Free Quote",
        "fr": "Demander un Devis Gratuit"
    },
    
    # Testimonials
    "O Que Dizem os Nossos Clientes": {
        "en": "What Our Clients Say",
        "fr": "Ce Que Disent Nos Clients"
    },
    "Cliente": {
        "en": "Client",
        "fr": "Client"
    },
    
    # Process
    "Como Fazemos a Sua Encomenda": {
        "en": "How We Make Your Order",
        "fr": "Comment Nous Réalisons Votre Commande"
    },
    "Simples, rápido e personalizado": {
        "en": "Simple, fast and personalized",
        "fr": "Simple, rapide et personnalisé"
    },
    "Contacte-nos": {
        "en": "Contact Us",
        "fr": "Contactez-nous"
    },
    "Ligue, envie mensagem no WhatsApp ou preencha o formulário. Conte-nos sobre o seu evento e as suas ideias.": {
        "en": "Call, WhatsApp or fill out the form. Tell us about your event and your ideas.",
        "fr": "Appelez, WhatsApp ou remplissez le formulaire. Parlez-nous de votre événement et de vos idées."
    },
    "Design & Orçamento": {
        "en": "Design & Quote",
        "fr": "Design & Devis"
    },
    "Criamos um design personalizado para si e apresentamos um orçamento detalhado. Ajustamos até ficar perfeito!": {
        "en": "We create a custom design for you and present a detailed quote. We adjust until it's perfect!",
        "fr": "Nous créons un design personnalisé pour vous et présentons un devis détaillé. Nous ajustons jusqu'à ce que ce soit parfait !"
    },
    "Produção Artesanal": {
        "en": "Artisan Production",
        "fr": "Production Artisanale"
    },
    "Preparamos o seu bolo com ingredientes premium, atenção aos detalhes e muito amor. Cada elemento é feito à mão.": {
        "en": "We prepare your cake with premium ingredients, attention to detail and lots of love. Every element is handmade.",
        "fr": "Nous préparons votre gâteau avec des ingrédients premium, une attention aux détails et beaucoup d'amour. Chaque élément est fait à la main."
    },
    "Entrega ou Recolha": {
        "en": "Delivery or Pickup",
        "fr": "Livraison ou Retrait"
    },
    "Entregamos no local do evento ou pode recolher no nosso atelier. O seu bolo chega perfeito para o grande momento!": {
        "en": "We deliver to the event venue or you can pick up at our studio. Your cake arrives perfect for the big moment!",
        "fr": "Nous livrons sur le lieu de l'événement ou vous pouvez retirer à notre atelier. Votre gâteau arrive parfait pour le grand moment !"
    },
    
    # Flavors
    "Sabores Irresistíveis": {
        "en": "Irresistible Flavors",
        "fr": "Saveurs Irrésistibles"
    },
    "Chocolate Belga": {
        "en": "Belgian Chocolate",
        "fr": "Chocolat Belge"
    },
    "Chocolate premium de alta qualidade": {
        "en": "Premium high-quality chocolate",
        "fr": "Chocolat premium de haute qualité"
    },
    "Baunilha Madagascar": {
        "en": "Madagascar Vanilla",
        "fr": "Vanille de Madagascar"
    },
    "Baunilha autêntica pura": {
        "en": "Pure authentic vanilla",
        "fr": "Vanille authentique pure"
    },
    "Red Velvet": {
        "en": "Red Velvet",
        "fr": "Red Velvet"
    },
    "Clássico aveludado com cream cheese": {
        "en": "Classic velvety with cream cheese",
        "fr": "Classique velouté avec cream cheese"
    },
    "Limão Siciliano": {
        "en": "Sicilian Lemon",
        "fr": "Citron de Sicile"
    },
    "Fresco e aromático": {
        "en": "Fresh and aromatic",
        "fr": "Frais et aromatique"
    },
    "Morango Fresco": {
        "en": "Fresh Strawberry",
        "fr": "Fraise Fraîche"
    },
    "Morangos naturais e creme": {
        "en": "Natural strawberries and cream",
        "fr": "Fraises naturelles et crème"
    },
    "Noz & Caramelo": {
        "en": "Walnut & Caramel",
        "fr": "Noix & Caramel"
    },
    "Doce de leite e nozes tostadas": {
        "en": "Dulce de leche and toasted walnuts",
        "fr": "Dulce de leche et noix grillées"
    },
    "Café Expresso": {
        "en": "Espresso Coffee",
        "fr": "Café Expresso"
    },
    "Sabor intenso de café": {
        "en": "Intense coffee flavor",
        "fr": "Saveur de café intense"
    },
    "Pistache": {
        "en": "Pistachio",
        "fr": "Pistache"
    },
    "Delicado e sofisticado": {
        "en": "Delicate and sophisticated",
        "fr": "Délicat et sophistiqué"
    },
    "Ferrero Rocher": {
        "en": "Ferrero Rocher",
        "fr": "Ferrero Rocher"
    },
    "Avelã e chocolate ao leite": {
        "en": "Hazelnut and milk chocolate",
        "fr": "Noisette et chocolat au lait"
    },
    "Oreo": {
        "en": "Oreo",
        "fr": "Oreo"
    },
    "Biscoito crocante e creme": {
        "en": "Crunchy cookie and cream",
        "fr": "Biscuit croquant et crème"
    },
    "Coco": {
        "en": "Coconut",
        "fr": "Noix de Coco"
    },
    "Tropical e refrescante": {
        "en": "Tropical and refreshing",
        "fr": "Tropical et rafraîchissant"
    },
    "Framboesa": {
        "en": "Raspberry",
        "fr": "Framboise"
    },
    "Frutos vermelhos frescos": {
        "en": "Fresh red berries",
        "fr": "Fruits rouges frais"
    },
    "Nutella": {
        "en": "Nutella",
        "fr": "Nutella"
    },
    "Cremoso e irresistível": {
        "en": "Creamy and irresistible",
        "fr": "Crémeux et irrésistible"
    },
    "Trufa Negra": {
        "en": "Black Truffle",
        "fr": "Truffe Noire"
    },
    "Chocolate extra negro": {
        "en": "Extra dark chocolate",
        "fr": "Chocolat extra noir"
    },
    "Maracujá": {
        "en": "Passion Fruit",
        "fr": "Fruit de la Passion"
    },
    "Exótico e tropical": {
        "en": "Exotic and tropical",
        "fr": "Exotique et tropical"
    },
    "Kinder Bueno": {
        "en": "Kinder Bueno",
        "fr": "Kinder Bueno"
    },
    "Wafer crocante e creme": {
        "en": "Crunchy wafer and cream",
        "fr": "Gaufrette croquante et crème"
    },
    "Sugestão especial? Fale connosco!": {
        "en": "Special suggestion? Contact us!",
        "fr": "Suggestion spéciale ? Contactez-nous !"
    },
    
    # Contact
    "Vamos Criar Algo Mágico Juntos": {
        "en": "Let's Create Something Magical Together",
        "fr": "Créons Quelque Chose de Magique Ensemble"
    },
    "Informações de Contacto": {
        "en": "Contact Information",
        "fr": "Informations de Contact"
    },
    "Morada": {
        "en": "Address",
        "fr": "Adresse"
    },
    "Horário de Encomendas": {
        "en": "Order Hours",
        "fr": "Heures de Commande"
    },
    "48h de antecedência mínima": {
        "en": "48h minimum advance notice",
        "fr": "48h de préavis minimum"
    },
    "O Seu Nome": {
        "en": "Your Name",
        "fr": "Votre Nom"
    },
    "Digite o seu nome completo": {
        "en": "Enter your full name",
        "fr": "Entrez votre nom complet"
    },
    "O Seu Email": {
        "en": "Your Email",
        "fr": "Votre Email"
    },
    "seuemail@exemplo.com": {
        "en": "youremail@example.com",
        "fr": "votreemail@exemple.com"
    },
    "Telefone/WhatsApp": {
        "en": "Phone/WhatsApp",
        "fr": "Téléphone/WhatsApp"
    },
    "+351 XXX XXX XXX": {
        "en": "+351 XXX XXX XXX",
        "fr": "+351 XXX XXX XXX"
    },
    "Tipo de Evento": {
        "en": "Event Type",
        "fr": "Type d'Événement"
    },
    "Selecione o tipo de evento": {
        "en": "Select event type",
        "fr": "Sélectionnez le type d'événement"
    },
    "Aniversário Infantil": {
        "en": "Children's Birthday",
        "fr": "Anniversaire d'Enfant"
    },
    "Aniversário Adulto": {
        "en": "Adult Birthday",
        "fr": "Anniversaire d'Adulte"
    },
    "Casamento": {
        "en": "Wedding",
        "fr": "Mariage"
    },
    "Batizado/Comunhão": {
        "en": "Baptism/Communion",
        "fr": "Baptême/Communion"
    },
    "Evento Corporativo": {
        "en": "Corporate Event",
        "fr": "Événement d'Entreprise"
    },
    "Outro": {
        "en": "Other",
        "fr": "Autre"
    },
    "Data do Evento": {
        "en": "Event Date",
        "fr": "Date de l'Événement"
    },
    "A Sua Mensagem": {
        "en": "Your Message",
        "fr": "Votre Message"
    },
    "Conte-nos sobre o seu evento, tema desejado, número de pessoas, cores preferidas, etc.": {
        "en": "Tell us about your event, desired theme, number of guests, preferred colors, etc.",
        "fr": "Parlez-nous de votre événement, thème souhaité, nombre d'invités, couleurs préférées, etc."
    },
    "Aceito a Política de Privacidade": {
        "en": "I accept the Privacy Policy",
        "fr": "J'accepte la Politique de Confidentialité"
    },
    "Enviar Pedido de Orçamento": {
        "en": "Send Quote Request",
        "fr": "Envoyer une Demande de Devis"
    },
    
    # CTA Section
    "Pronto Para o Bolo dos Seus Sonhos?": {
        "en": "Ready for Your Dream Cake?",
        "fr": "Prêt pour le Gâteau de Vos Rêves ?"
    },
    "Vamos tornar o seu evento ainda mais especial com um bolo personalizado que todos vão adorar": {
        "en": "Let's make your event even more special with a custom cake that everyone will love",
        "fr": "Rendons votre événement encore plus spécial avec un gâteau personnalisé que tout le monde adorera"
    },
    "Fazer Encomenda Agora": {
        "en": "Order Now",
        "fr": "Commander Maintenant"
    },
    "Resposta garantida em 24h": {
        "en": "Response guaranteed within 24h",
        "fr": "Réponse garantie sous 24h"
    },
    
    # Footer
    "by Daisy": {
        "en": "by Daisy",
        "fr": "par Daisy"
    },
    "Criando momentos deliciosos e memoráveis desde 2018. Cada bolo é feito com amor, dedicação e ingredientes premium.": {
        "en": "Creating delicious and memorable moments since 2018. Every cake is made with love, dedication and premium ingredients.",
        "fr": "Créer des moments délicieux et mémorables depuis 2018. Chaque gâteau est fait avec amour, dévouement et des ingrédients premium."
    },
    "Links Rápidos": {
        "en": "Quick Links",
        "fr": "Liens Rapides"
    },
    "Informação": {
        "en": "Information",
        "fr": "Information"
    },
    "Política de Privacidade": {
        "en": "Privacy Policy",
        "fr": "Politique de Confidentialité"
    },
    "Termos e Condições": {
        "en": "Terms and Conditions",
        "fr": "Termes et Conditions"
    },
    "FAQs": {
        "en": "FAQs",
        "fr": "FAQs"
    },
    "Blog": {
        "en": "Blog",
        "fr": "Blog"
    },
    "Receba Novidades": {
        "en": "Receive News",
        "fr": "Recevoir des Nouvelles"
    },
    "Subscreva para receber ofertas exclusivas, novidades e inspiração diretamente no seu email.": {
        "en": "Subscribe to receive exclusive offers, news and inspiration directly to your email.",
        "fr": "Abonnez-vous pour recevoir des offres exclusives, des nouvelles et de l'inspiration directement dans votre email."
    },
    "Seu email": {
        "en": "Your email",
        "fr": "Votre email"
    },
    "Subscrever": {
        "en": "Subscribe",
        "fr": "S'abonner"
    },
    "Todos os direitos reservados.": {
        "en": "All rights reserved.",
        "fr": "Tous droits réservés."
    },
    "Desenvolvido por": {
        "en": "Developed by",
        "fr": "Développé par"
    }
}

# Print total
print(f"Total translations: {len(translations)}")
print("\nSample entries:")
for i, (pt, trans) in enumerate(list(translations.items())[:5]):
    print(f"{i+1}. PT: {pt}")
    print(f"   EN: {trans['en']}")
    print(f"   FR: {trans['fr']}")
    print()
