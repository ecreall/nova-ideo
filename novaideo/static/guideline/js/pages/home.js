
$(document).ready(function(){
    var _ = NovaIdeoGuideline._;
    var novaideo_home_guide = new Guideline.Guide("novaideo_home", {
        memoizeLasStep: true
    });

    var homePage = novaideo_home_guide.addPage("index");
    var novaideolog = 'http://0.0.0.0:6543/novaideostatic/images/novaideo_logo.png';
    homePage.addStep({
        type: "overlay",
        title: "<div>"+_("Welcome to")+
               " <img alt='Nova-Ideo' src='"+novaideolog+"' class='globe-logo'> Nova-Ideo</div>",
        showSkip: false,
        content: (
            "<p>"+
              _("<strong>Nova-Ideo</strong> is a platform implementing a complete process, "+
                "in which working groups transform ideas into complete proposals with "+
                "a system of amendment and voting sessions. C'est le moyen pour vous exprimer par excellence.")+
            "</p>"+
            "<button class='gl-continue btn btn-primary btn-alpha-blue hide-button'>"+
              "<i class='glyphicon glyphicon-play'></i> "+
              _("Amazing... Show me more!")+
            "</button>"+
            "<br/>"+
            "<a href='#' class='gl-skip'>"+_("I don't care. Skip this.")+"</a>"
        )
    });

    homePage.addStep({
        type: "overlay",
        title: _("Ask a questions or add a new idea"),
        content: (
            "<p>"+
              _("Ce formulaire vous permet d'ajouter une idée ou poser une question.")+
            "</p>"
        ),
        showAt: ".home-add-content-container",
        align: "center bottom",
        continueHtml: NovaIdeoGuideline.next_btn,
        previousHtml: NovaIdeoGuideline.prev_btn,
        stepControlContainer: NovaIdeoGuideline.stepControlContainer,
        showContinue: true,
        showPrevious: true,
        scrollToItem: true,
    },
    function(){
        return $(".home-add-content-container").length>0;
    });



    homePage.addStep({
        type: "overlay",
        title: _("Questions"),
        content: (
            "<p>"+
              _("Vous trouvez ici les questions posées les membres de la plateforme. Vous pouvez y répondre, les soutenir ou les discuter.")+
            "</p>"
        ),
        showAt: "#home-questions-counter",
        align: "center top",
        continueHtml: NovaIdeoGuideline.next_btn,
        previousHtml: NovaIdeoGuideline.prev_btn,
        stepControlContainer: NovaIdeoGuideline.stepControlContainer,
        showContinue: true,
        showPrevious: true,
        scrollToItem: true,
    });

    

    homePage.addStep({
        type: "overlay",
        title: _("Ideas"),
        content: (
            "<p>"+
              _("Vous trouvez ici les idées ajoutées par les membres de la plateforme. Vous pouvez les soutenir ou les discuter.")+
            "</p>"
        ),
        showAt: "#home-ideas-counter",
        align: "center top",
        continueHtml: NovaIdeoGuideline.next_btn,
        previousHtml: NovaIdeoGuideline.prev_btn,
        stepControlContainer: NovaIdeoGuideline.stepControlContainer,
        showContinue: true,
        showPrevious: true,
        scrollToItem: true,
    });

    homePage.addStep({
        type: "overlay",
        title: _("Working groups"),
        content: (
            "<p>"+
              _("Vous trouvez ici les groupes de travail crée par les membres de la plateforme. Vous pouvez y participer, les soutenir ou les discuter.")+
            "</p>"
        ),
        showAt: "#home-proposals-counter",
        align: "center top",
        continueHtml: NovaIdeoGuideline.next_btn,
        previousHtml: NovaIdeoGuideline.prev_btn,
        stepControlContainer: NovaIdeoGuideline.stepControlContainer,
        showContinue: true,
        showPrevious: true,
        scrollToItem: true,
    },
    function(){
        return $("#home-proposals-counter").length>0;
    });

    homePage.addStep({
        type: "overlay",
        title: _("Your contents"),
        content: (
            "<p>"+
              _("Vous trouvez ici les liens vous permettant d'accéder à vos contenus, vos groupes de travail, vos appréciations ou vos suivies.")+
            "</p>"
        ),
        showAt: ".access-menu ul.nav.navbar-nav",
        align: "center bottom",
        continueHtml: NovaIdeoGuideline.next_btn,
        previousHtml: NovaIdeoGuideline.prev_btn,
        stepControlContainer: NovaIdeoGuideline.stepControlContainer,
        showContinue: true,
        showPrevious: true,
        scrollToItem: true,
    });

    homePage.addStep({
        type: "overlay",
        title: _("Vos alerts"),
        content: (
            "<p>"+
              _("Vous trouvez ici toutes les alertes concernant votre activité.")+
            "</p>"
        ),
        showAt: ".hidden-xs.alert-block",
        align: "center bottom",
        continueHtml: NovaIdeoGuideline.next_btn,
        previousHtml: NovaIdeoGuideline.prev_btn,
        stepControlContainer: NovaIdeoGuideline.stepControlContainer,
        showContinue: true,
        showPrevious: true,
    },
    function(){
        return $(".alert-block").length>0;
    });

    homePage.addStep({
        title: _("Accedez à vos discussions"),
        content: (
            "<p>"+
              _("Vous trouvez ici les discussions auxquelles vous participez. <span class='gl-target-click'>Veuillez cliquer sur l'icône <span class='ion-chatbubbles'></span> pour continuer.</span>")+
            "</p>"
        ),
        showAt: ".all-channels-toggle:not(.close)",
        align: "right middle",
        previousHtml: NovaIdeoGuideline.prev_btn,
        stepControlContainer: NovaIdeoGuideline.stepControlContainer,
        showPrevious: true,
    },
    function(){
        return $(".all-channels.toggled").length>0;
    });

    homePage.addStep({
        type: "overlay",
        title: _("Discussions générales et privées"),
        content: (
            "<p>"+
              _("Les discussions générales sont visibles par tous les membres et les discussions privées sont visibles que par vous et votre interlocuteur.")+
            "</p>"
        ),
        showAt: ".all-channels .all-channels-container",
        align: "right middle",
        continueHtml: NovaIdeoGuideline.next_btn,
        previousHtml: NovaIdeoGuideline.prev_btn,
        stepControlContainer: NovaIdeoGuideline.stepControlContainer,
        showContinue: true,
        showPrevious: true,
        showAfter: $(".all-channels.toggled").length == 0? 0: 0.5
    },
    function(){
        return $(".all-channels").length > 0;
    });
    
    var has_menu = $(".menu-toggle.top").length>0;
    if(has_menu){
        homePage.addStep({
            title: _("Votre menue"),
            content: (
                "<p>"+
                  _("Vous trouvez ici les différente actions d'ajout d'acces ou de modification. <span class='gl-target-click'>Veuillez cliquer sur l'icône <span class='glyphicon glyphicon-menu-hamburger'></span> pour continuer.</span>")+
                "</p>"
            ),
            showAt: ".menu-toggle.top",
            align: "center bottom",
            previousHtml: NovaIdeoGuideline.prev_btn,
            stepControlContainer: NovaIdeoGuideline.stepControlContainer,
            showPrevious: true,
        },
        function(){
            return $(".sidebar-background.toggled").length == 0;
        });

        var has_configure_btn = $("#adminprocess-configure_site-btn").length > 0;

        homePage.addStep({
            title: _("Autres actions"),
            content: (
                "<p>"+
                  _("Vous trouvez dans le sous-menu <strong>Plus</strong> d'autres actions comme la configuration ou l'extraction de votre contenu. <span class='gl-target-click'>Veuillez cliquer sur le sous-menu <strong><span class='glyphicon glyphicon-cog'></span> Plus</strong> pour continuer.</span>")+
                "</p>"
            ),
            showAt: "#Plus-btn",
            align: "right middle",
            continueHtml: has_configure_btn? null: NovaIdeoGuideline.end_btn,
            previousHtml: NovaIdeoGuideline.prev_btn,
            stepControlContainer: NovaIdeoGuideline.stepControlContainer,
            showPrevious: true,
            showContinue: !has_configure_btn,
            showAfter: 0.5
        },
        function(){
            return has_configure_btn && $("#Plus-btn.active-item").length == 0;
        });

        homePage.addStep({
            type: "overlay",
            title: _("Configurer votre application"),
            content: (
                "<p>"+
                  _("Vous pouvez configurer le comportement de votre instance comme la spécification des contenus à modérer, les contenus à soutenir ou à examiner. Vous pouvez aussi configurer l'interface utilisateur en ajoutant votre logo...")+
                "</p>"
            ),
            showAt: "#adminprocess-configure_site-btn",
            align: "right middle",
            continueHtml: NovaIdeoGuideline.next_btn,
            previousHtml: NovaIdeoGuideline.prev_btn,
            stepControlContainer: NovaIdeoGuideline.stepControlContainer,
            showContinue: true,
            showPrevious: true,
        },
        function(){
            return has_configure_btn;
        });
    }

    homePage.addStep({
        title: _("Aide contextuelle"),
        content: (
            "<p>"+
              _("Nous vous proposons aussi une aide contextuelle vous permettant d'avoir des informations contextualisées.")+
            "</p>"
        ),
        showAt: ".contextual-help-toggle",
        align: "left middle",
        continueHtml: NovaIdeoGuideline.end_btn,
        previousHtml: NovaIdeoGuideline.prev_btn,
        stepControlContainer: NovaIdeoGuideline.stepControlContainer,
        showContinue: true,
        showPrevious: true,
        scrollToItem: true,
    });

    homePage.addStep({
        type: "overlay",
        title: _("Maintenant, c'est à vous de créer l'information !"),
        showSkip: false,
        content: (
            "<p>"+_("Poser des questions, ajouter des idées, travailler en groupe ou débattre cela ne tient qu'à vous !")+"</p>"+
            "<br/>"+
            "<button class='gl-continue btn btn-primary btn-alpha-blue hide-button'>"+
              "<i class='glyphicon glyphicon-off'></i> "+
              "<strong>"+_("Merci et à bientôt !")+"</strong>"+
            "</button>"
        )
    });

  novaideo_home_guide.register();

  NovaIdeoGuideline.start("novaideo_home", "index");

});