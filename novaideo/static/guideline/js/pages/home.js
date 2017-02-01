
$(document).ready(function(){
    NovaIdeoGuideline.init();
    var _ = NovaIdeoGuideline._;
    var novaideo_home_guide = new Guideline.Guide("novaideo_home", {
        memoizeLasStep: true
    });

    var homePage = novaideo_home_guide.addPage("index");
    var novaideolog = NovaIdeoGuideline.logo_url;
    homePage.addStep({
        type: "overlay",
        title: "<div>"+_("Welcome to")+
               " <img alt='Nova-Ideo' src='"+novaideolog+"' class='globe-logo'> Nova-Ideo</div>",
        showSkip: false,
        content: (
            "<p class='hidden-xs'>"+
              _("NovaIdeo Description")+
            "</p>"+
            "<p style='color: #54d0ff'>"+
              _("This is a guided tour to show you the essentials of <strong>Nova-Ideo</strong>. The visit will only take a few seconds.")+
            "</p>"+
            "<button class='gl-continue btn btn-primary btn-alpha-blue hide-button'>"+
              "<i class='glyphicon glyphicon-play'></i> "+
              _("Let's go!")+
            "</button>"+
            "<br/>"+
            "<a href='#' class='gl-skip'>"+_("No thanks!")+"</a>"
        )
    });

    homePage.addStep({
        type: "overlay",
        title: "<span class='glyphicon glyphicon-pencil'></span> "+ _("Ask a question, add a poll or a new idea"),
        content: (
            "<p>"+
              _("This form allows you to add an idea, ask a question or add a poll. A poll is a question with options.")+
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
        title: "<span class='md md-live-help'></span> "+ _("The questions"),
        content: (
            "<p>"+
              _("You will find here the questions asked by the members of the platform. You can answer, support or discuss them.")+
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
        title: "<span class='icon novaideo-icon icon-idea'></span> "+ _("The ideas"),
        content: (
            "<p>"+
              _("You will find here the ideas added by the members of the platform. You can support or discuss them.")+
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
        title: "<span class='icon novaideo-icon icon-wg'></span> "+ _("The working groups"),
        content: (
            "<p>"+
              _("You will find here the working groups created by the members of the platform. You can participate, support or discuss them.")+
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
        title: "<span class='glyphicon glyphicon-list'></span> "+ _("Your contents"),
        content: (
            "<p>"+
              _("You will find here the links allowing you to access your contents, your working groups, your evaluations or your followings.")+
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
        title: "<span class='icon glyphicon glyphicon-bell'></span> "+ _("Your notifications"),
        content: (
            "<p>"+
              _("You will find here all the notifications concerning your activity.")+
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
        title: "<span class=' ion-chatbubbles'></span> "+ _("Access to your discussions"),
        content: (
            "<p>"+
              _("You will find here the discussions you participate in. <span class='gl-target-click'>Please click on this icon <span class='ion-chatbubbles'></span> to continue.</span>")+
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
        title: "<span class=' ion-chatbubbles'></span> "+ _("General and private discussions"),
        content: (
            "<p>"+
              _("General discussions are visible by all members and private discussions are visible only by you and your interlocutor.")+
            "</p>"
        ),
        showAt: ".all-channels .all-channels-container",
        align: "right middle",
        continueHtml: NovaIdeoGuideline.next_btn,
        stepControlContainer: NovaIdeoGuideline.stepControlContainer,
        showContinue: true,
        showAfter: $(".all-channels.toggled").length == 0? 0: 0.5
    },
    function(){
        return $(".all-channels").length > 0;
    });
    
    var has_menu = $(".menu-toggle.top").length>0;
    if(has_menu){
        homePage.addStep({
            title:"<span class='glyphicon glyphicon-menu-hamburger'></span> "+ _("Your menu"),
            content: (
                "<p>"+
                  _("You will find here the different actions allowing you to add, access or modify contents. <span class='gl-target-click'>Please click on this icon <span class='glyphicon glyphicon-menu-hamburger'></span> to continue.</span>")+
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
            title: "<span class='glyphicon glyphicon-cog'></span> "+ _("Other actions"),
            content: (
                "<p>"+
                  _("You can find other actions in the <strong> More </strong> submenu such as configuring or extracting your content. <span class='gl-target-click'>Please click on this icon <strong><span class='glyphicon glyphicon-cog'></span> More</strong> to continue.</span>")+
                "</p>"
            ),
            showAt: "#More-btn",
            align: "right middle",
            continueHtml: has_configure_btn? null: NovaIdeoGuideline.end_btn,
            stepControlContainer: NovaIdeoGuideline.stepControlContainer,
            showContinue: !has_configure_btn,
            showAfter: 0.5
        },
        function(){
            return has_configure_btn && $("#More-btn.active-item").length == 0;
        });

        homePage.addStep({
            type: "overlay",
            title: "<span class='glyphicon glyphicon-wrench'></span> "+ _("Configuring your application"),
            content: (
                "<p>"+
                  _("You can configure the behavior of your instance such as specifying content to moderate, content to support or examine. You can also configure the user interface by adding your logo...")+
                "</p>"
            ),
            showAt: "#adminprocess-configure_site-btn",
            align: "right middle",
            continueHtml: NovaIdeoGuideline.next_btn,
            stepControlContainer: NovaIdeoGuideline.stepControlContainer,
            showContinue: true,
        },
        function(){
            return has_configure_btn;
        });
    }

    homePage.addStep({
        title: "<span class='glyphicon glyphicon-info-sign'></span> "+ _("Contextual help"),
        content: (
            "<p>"+
              _("We also offer context-sensitive help for contextualized informations.")+
            "</p>"
        ),
        showAt: ".contextual-help-toggle-container",
        align: "left middle",
        continueHtml: NovaIdeoGuideline.end_btn,
        previousHtml: NovaIdeoGuideline.prev_btn,
        stepControlContainer: NovaIdeoGuideline.stepControlContainer,
        showContinue: true,
        showPrevious: true,
        scrollToItem: true,
        function(){
            return $('.contextual-help-toggle-container').length > 0;
        }
    });

    homePage.addStep({
        type: "overlay",
        title: "<span style='color: #337ab7'>"+_("Now it's up to you to create the information!")+"</span>",
        showSkip: false,
        content: (
            "<p class='hidden-xs'>"+_("Ask questions, add ideas, work in groups or debate ... it's up to you!")+"</p>"+
            "<p class='hidden-xs'>"+_("We have just presented you the essential to be able to start, many other features are available to improve your productivity.")+
            "<ul class='list-unstyled'>"+
                "<li>"+_("For more information, please go to <a href='https://www.nova-ideo.com/'>nova-ideo.com</a>.")+"</li>"+
                "<li>"+_("To follow <strong>Nova-Ideo</strong>, join us on <a href='https://twitter.com/NovaIdeo'>twitter</a>.")+"</li>"+
                "<li>"+_("To suggest improvements, please register on <a href='https://evolutions.nova-ideo.com/'>Nova-Ideo Evolutions</a>.")+"</li>"+
            "</ul></p>"+
            "<div style='margin-bottom: 10px;'><img alt='Nova-Ideo' src='"+novaideolog+"' class='globe-logo'></div>"+
            "<button class='gl-continue btn btn-primary btn-alpha-blue hide-button'>"+
              "<i class='glyphicon glyphicon-off'></i> "+
              "<strong>"+_("Thank you and see you soon!")+"</strong>"+
            "</button>"
        )
    });

  novaideo_home_guide.register();

  NovaIdeoGuideline.start("novaideo_home", "index");

});