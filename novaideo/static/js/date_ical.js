/* authors: Charles Seymour, Vincent Fretin and Amen SOUISSI */

var date_help_write_data = {};


function init_date_help_data(oid){
	date_help_write_data[oid] = {}
	var todaydate = new Date();
	date_help_write_data[oid].todaydate=todaydate;
	date_help_write_data[oid].curmonth=todaydate.getMonth()+1; //get current month (1-12)
	date_help_write_data[oid].curyear=todaydate.getFullYear(); //get current year

	date_help_write_data[oid].ymdc = '';		// year month day current: 23 décembre 2007
	date_help_write_data[oid].de_A = '';		// "de"|"à"
	date_help_write_data[oid].heuresMinutes = '';	// "à" mode: 15h; "de" mode: 15h à 18h
	date_help_write_data[oid].heuresMinutesEtDe = ''; // et de 20h à 22h
	date_help_write_data[oid].choixMode = 0; // 1, 2, 3 or 4
	date_help_write_data[oid].choix = ''; // "Le"|"Les"|"Du...Au..."|"Jusqu'au"
	date_help_write_data[oid].modeChecked = false;
	date_help_write_data[oid].choixDate = false;

	// "Du..Au" mode
	date_help_write_data[oid].choixDu = false;
	date_help_write_data[oid].DuPart = ''; // Du 2 décembre 2007

	// "Les" mode
	date_help_write_data[oid].index;
	date_help_write_data[oid].tab;

	// constants
	date_help_write_data[oid].DAY = 0;
	date_help_write_data[oid].MONTH = 1;
	date_help_write_data[oid].YEAR = 2;
};


//*****************************************************Templates******************************************************

function buildADe(oid)
{
	var t = '<div><br/>';
	t += '<div><div class="date-horaire-select" ><label><input type="radio" name="horaire1" id=\"'+oid+'selectA" value="à" onclick="affHoraires(\'à\',\''+oid+'\')" />&nbsp;&nbsp;à</label></div>';
    t += '<div class="date-horaire" id="'+oid+'HorairesA"></div></div>';
	t += '<br /><br />';
	t += '<div><div class="date-horaire-select" ><label><input type="radio" name="horaire1" id=\"'+oid+'selectDe" value="de" onclick="affHoraires(\'de\', \''+oid+'\')" />&nbsp;de</label></div>';
	t += '<div class="date-horaire" id="'+oid+'HorairesDe"></div>';
	t += '<div class="date-choice-etde" id="'+oid+'choixEtDe"></div>';
    t+=	'</div>';
	t += '</div>';
	return t;
}


function buildHoraireEtDe(oid)
{
	// Ici je contruis les listes déroulantes : Heures Minutes
	
	var t='<div>';
	t+='&nbsp;&nbsp;&nbsp;<select name="heures3" id=\"'+oid+'horaire_heures3" onchange="lhoraireetde(\''+oid+'\')">';
	t+='<option value="--">--</option>';
	for (var i=0; i<24; i++)
	{
		t+='<option value="'+i+'">'+i+'</option>';
	}
	
	t+='</select>h ';
	t+='<select name="minutes3" id=\"'+oid+'horaire_minutes3" onchange="lhoraireetde(\''+oid+'\')">';
	t+='<option value="">--</option>';
    var r;
	for (var j=0; j<60; j=j+5)
	{
		r = j;
		if (j<10) { r='0'+j; }
		t+='<option value="'+r+'">'+r+'</option>';
	}

	t+='</select><br />à ';
	t+='<select name="heures4" id=\"'+oid+'horaire_heures4" onchange="lhoraireetde(\''+oid+'\')">';
	t+='<option value="--">--</option>';
	for (var k=0; k<24; k++)
	{
		t+='<option value="'+k+'">'+k+'</option>';
	}
	t+='</select>h ';
	t+='<select name="minutes4" id=\"'+oid+'horaire_minutes4" onchange="lhoraireetde(\''+oid+'\')">';
	t+='<option value="">--</option>';
	for (var l=0; l<60; l=l+5)
	{
		r = l;
		if (l<10) { r='0'+l; }
		t+='<option value="'+r+'">'+r+'</option>';
	}	
	t+='</select>';
	t+='</div>';

	return t;

}


function buildHoraireDeA(oid)
{
	var t='<div>';
	t+='&nbsp;&nbsp;&nbsp;<select name="heures1" id=\"'+oid+'horaire_heures1" onchange="lHoraireDeA(\''+oid+'\')">';
	t+='<option value="--">--</option>';
    var i, r;
	for (i=0; i<24; i++)
	{
		t+='<option value="'+i+'">'+i+'</option>';
	}
	
	t+='</select>h ';
	t+='<select name="minutes1" id=\"'+oid+'horaire_minutes1" onchange="lHoraireDeA(\''+oid+'\')">';
	t+='<option value="">--</option>';
	for (i=0; i<60; i=i+5)
	{
		r = i;
		if (i<10) { r='0'+i; }
		t+='<option value="'+r+'">'+r+'</option>';
	}

	t+='</select><br />à ';

	t+='<select name="heures2" id=\"'+oid+'horaire_heures2" onchange="lHoraireDeA(\''+oid+'\')">';
	t+='<option value="--">--</option>';
	
	for (i=0; i<24; i++)
	{
		t+='<option value="'+i+'">'+i+'</option>';
	}
	
	t+='</select>h ';
	t+='<select name="minutes2" id=\"'+oid+'horaire_minutes2" onchange="lHoraireDeA(\''+oid+'\')">';
	t+='<option value="">--</option>';
	for (i=0; i<60; i=i+5)
	{
		r = i;
		if (i<10) { r='0'+i; }
		t+='<option value="'+r+'">'+r+'</option>';
	};	
    t+='</select>';
	t+='</div>';

	return t;
}


function buildHoraireA(funcJs, oid)
{
	// Ici je contruis les listes déroulantes : Heures Minutes
	
	var t='<div>';
	t+='<select name="heures" id=\"'+oid+'horaire_heures" onchange="'+funcJs+'">';
	t+='<option value="--">--</option>';
	
    var i;
	for (i=0; i<24; i++)
	{
			t+='<option value="'+i+'">'+i+'</option>';
	}
	
	t+='</select>h ';
	t+='<select name="minutes" id=\"'+oid+'horaire_minutes" onchange="'+funcJs+'">';
	t+='<option value="">--</option>';
	for (i=0; i<60; i=i+5)
	{
		var r = i;
		if (i<10) { r='0'+i; }
		t+='<option value="'+r+'">'+r+'</option>';
	}	
	t+='</select>';
	t+='</div>';

	return t;
}


function buildEtDe(oid)
{

	var t = '<div class="date-horaire-select" ><label><input type="radio" name="horaireEtDe" id=\"'+oid+'formulaireEtDe" value="etDe" onclick="affHorairesEtDe(\''+oid+'\')" />&nbsp;et de</label></div>';
	t += '<div class="date-horaire" id="'+oid+'HorairesEtDe"></div>';

	return t;
}


//*****************************************************Help operations******************************************************

function selectMode(mode, element)
{
	var oid = $($(element).parents('.helpWriteSeances').first()).attr('id');
    oid = oid.replace('helpWriteSeances', '');
    var _ = date_help_write_data[oid];
	_.choix = document.getElementById(oid+'choixPeriode'+mode).value;
	_.choIxmode = mode;
	_.moDechecked = true;
	_.choIxdate = false;
	resetAffichage(oid);
	document.getElementById(oid+"SortirCalendar").innerHTML = buildCal(_.curmonth,_.curyear,oid);
	if (mode == 1)
	{
		document.getElementById(oid+"choixADe").innerHTML = buildADe(oid);
	}

	if (mode == 2)
	{
		resetTabLes(oid);
		document.getElementById(oid+"choixADe").innerHTML = buildADe(oid);
	}

	if (mode == 3)
	{
		_.choIxDu = false;
		var label = '<span style="color:#408c40">Choisissez votre début de période</span>';
		document.getElementById(oid+"messageValidation").innerHTML = label;
	}

	if (mode == 4)
	{
		document.getElementById(oid+"choixADe").innerHTML = buildADe(oid);
	}
}

function resetAffichage(oid)
{
	var _ = date_help_write_data[oid];
	_.ymdc = '';
	_.dE_A = '';
	_.heurEsminutes='';
	_.heurEsminutEsEtDe='';

	var InputmSeances = document.getElementById(oid);
	if (InputmSeances){ InputmSeances.value=''; }
	
	var idName = new Array(6);
	// second line
	idName[0] = oid+"choixADe";
	idName[1] = oid+"Horaires";
	idName[2] = oid+"choixEtDe";
	
	// third line
	idName[4] = oid+"ListeDesDates";
	idName[5] = oid+"messageValidation";

	for (var i = 0; i < idName.length; i++)
	{
		if (document.getElementById(idName[i]))
		{
			document.getElementById(idName[i]).innerHTML='';
		}
	}
}


function lHoraire(oid) 
{
	var _ = date_help_write_data[oid];
	var horaire_heures = document.getElementById(oid+'horaire_heures');
	var horaire_minutes = document.getElementById(oid+'horaire_minutes');
	var filled = horaire_heures.selectedIndex;
	if (!filled) {
        return;
    }
	
	var heures = horaire_heures.value;
	var minutes = horaire_minutes.value;
	
	_.heurEsminutes = heures + 'h' + minutes;
	laDate(_.ymdc, oid);
}


function lHoraireDeA(oid)
{
	var _ = date_help_write_data[oid];
	var horaire_heures1 = document.getElementById(oid+'horaire_heures1');
	var horaire_minutes1 = document.getElementById(oid+'horaire_minutes1');
	var horaire_heures2 = document.getElementById(oid+'horaire_heures2');
	var horaire_minutes2 = document.getElementById(oid+'horaire_minutes2');
	var filled = horaire_heures1.selectedIndex && horaire_heures2.selectedIndex;
	if (!filled) {
        return;
    }
	
	var heures1 = horaire_heures1.value;
	var minutes1 = horaire_minutes1.value;

	var heures2 = horaire_heures2.value;
	var minutes2 = horaire_minutes2.value;

	_.heurEsminutes = heures1 + 'h' + minutes1 + ' à ' + heures2 + 'h' + minutes2;
	laDate(_.ymdc, oid);
}

function lhoraireetde(oid)
{
	var _ = date_help_write_data[oid];
	var horaire_heures3 = document.getElementById(oid+'horaire_heures3');
	var horaire_minutes3 = document.getElementById(oid+'horaire_minutes3');
	var horaire_heures4 = document.getElementById(oid+'horaire_heures4');
	var horaire_minutes4 = document.getElementById(oid+'horaire_minutes4');
	var filled = horaire_heures3.selectedIndex && horaire_heures4.selectedIndex;
	if (!filled) {
        return;
    }
	
	var heures3 = horaire_heures3.value;
	var minutes3 = horaire_minutes3.value;

	var heures4 = horaire_heures4.value;
	var minutes4 = horaire_minutes4.value;

	_.heurEsminutEsEtDe = ' et de ' + heures3 + 'h' + minutes3 + ' à ' + heures4 + 'h' + minutes4;
	laDate(_.ymdc, oid);
}


function affHoraires(pMode, oid)
{
	var _ = date_help_write_data[oid];
	if (!(_.moDechecked && _.choIxdate))
	{
		alert("Veuillez sélectionner une date dans le calendrier.");
		document.getElementById(oid+'selectA').checked = false;
		document.getElementById(oid+'selectDe').checked = false;
		return;
	}

	_.dE_A = '';
	_.heurEsminutes = '';
	_.heurEsminutEsEtDe = '';
	laDate(_.ymdc, oid);
	_.dE_A = pMode;

	document.getElementById(oid+"HorairesA").innerHTML = "";
	document.getElementById(oid+"HorairesDe").innerHTML = "";
	document.getElementById(oid+"choixEtDe").innerHTML = "";

	if (_.dE_A == "à")
	{
		var formHoraire = buildHoraireA("lHoraire(\'"+oid+"\')",oid);
		document.getElementById(oid+"HorairesA").innerHTML = formHoraire;
	}

	if (_.dE_A == "de")
	{
		var newCalendar3 = buildHoraireDeA(oid);
		document.getElementById(oid+"HorairesDe").innerHTML = newCalendar3;
	
		var newCalendar4 = buildEtDe(oid);
		document.getElementById(oid+"choixEtDe").innerHTML = newCalendar4;
	}
}


function affHorairesEtDe(oid)
{
	var _ = date_help_write_data[oid];
	var horaire_heures1 = document.getElementById(oid+'horaire_heures1');
	var horaire_heures2 = document.getElementById(oid+'horaire_heures2');
	var filled = horaire_heures1.selectedIndex && horaire_heures2.selectedIndex;
	if (!filled)
	{
		alert("Vous devez sélectionnez votre première tranche horaire !");
		document.getElementById(oid+"formulaireEtDe").checked = false;
		return;
	}

	laDate(_.ymdc, oid);

	document.getElementById(oid+"HorairesEtDe").innerHTML = buildHoraireEtDe(oid);
}



function affResultatJusquAu(ymd, oid)
{
	var _ = date_help_write_data[oid];
	var lDate = ymd.split(" ");
	var todaydate = new Date();
	var cur_year = todaydate.getFullYear();
	var sentence;
	if (cur_year == lDate[_.YEAR]) {
		sentence = _.choix + ' ' + lDate[_.DAY] + ' ' + lDate[_.MONTH];
	} else {
		sentence = _.choix + ' ' + ymd;
	}
	if (_.dE_A) { sentence += ' ' + _.dE_A + ' ' + _.heurEsminutes + _.heurEsminutEsEtDe; }
	document.getElementById(oid).value = sentence;
}


function affResultatLe(ymd, oid) /* formate le texte à afficher */
{
	var _ = date_help_write_data[oid];
	var lDate = ymd.split(" ");
	var todaydate = new Date();
	var cur_year = todaydate.getFullYear();
	var sentence;
	if (cur_year == lDate[_.YEAR]) {
		sentence = _.choix + ' ' + lDate[_.DAY] + ' ' + lDate[_.MONTH];
	} else {
		sentence = _.choix + ' ' + ymd;
	}
	if (_.dE_A) { sentence += ' ' + _.dE_A + ' ' + _.heurEsminutes + _.heurEsminutEsEtDe; }
	document.getElementById(oid).value = sentence;
}



/* début fonctions pour Du..Au */
function validDuPart(oid)	/* sav de la première période (Du .. )*/
{
	var _ = date_help_write_data[oid];
	_.choIxDu = true;
	_.choIxdate = false;

	var label = '<span style="color:#408c40">Choisissez votre fin de période</span>';
	document.getElementById(oid+"messageValidation").innerHTML = label;
	document.getElementById(oid+"choixADe").innerHTML = buildADe(oid);
	remove_selected(oid)
}


function affBarreDu(ymd, oid)	/* formate de la zone texte Du...*/
{
	var _ = date_help_write_data[oid];
	var sentence = 'Du' + ' ' + ymd;
	_.Dupart = ymd;
	document.getElementById(oid).value = sentence;

	var button = '<button class="btn btn-primary btn-xs" type="button" name="Validez" onclick="validDuPart(\''+oid+'\')"><span class="glyphicon glyphicon-play"></span> Valider le début de période</button>';
	document.getElementById(oid+"messageValidation").innerHTML = button;
}


function affBarreAu(ymd, oid)		/* formate de la zone texte Au... */ 
{
	var _ = date_help_write_data[oid];
	document.getElementById(oid+"messageValidation").innerHTML = '';

	var date1 = _.Dupart.split(" ");
	var date2 = ymd.split(" ");
	var todaydate = new Date();
	var cur_year = todaydate.getFullYear();
	var sentence = '';
	var p1 = '';
	var p2 = '';
	p2 = date2[_.DAY] + ' ' + date2[_.MONTH];
	if (date1[_.MONTH] == date2[_.MONTH]) { // same month
		p1 = date1[_.DAY];
	} else {
		p1 = date1[_.DAY] + ' ' + date1[_.MONTH];
	}
	if (date1[_.YEAR] != date2[_.YEAR]) {
		p1 += ' ' + date1[_.YEAR];
		p2 += ' ' + date2[_.YEAR];
	} else /**/if (date1[_.YEAR] != cur_year)/**/ { // if not this year
		p2 += ' ' + date2[_.YEAR];
	}
	sentence = 'Du ' + p1 + ' au ' + p2;
	if (_.dE_A) { sentence += ' ' + _.dE_A + ' ' + _.heurEsminutes + _.heurEsminutEsEtDe; }
	document.getElementById(oid).value = sentence;
}


/* fin fonctions pour Du..Au */


/* begin functions for "Les" mode */

function ajoutDatesLes(oid)
{
	var t = '<hr class="soften"><div>';
	t += '<div class="help-user-dates"><span class="glyphicon glyphicon-th-list"></span> Vos dates</div><div name="liste" id="'+oid+'listeDates" style="width:100%">';
	t += '</div>';
	t += '<p style="text-align:center; margin-top: 15px"><button type="button" class="btn btn-success btn-sm" name="Valider" onclick="generateLesSentence(\''+oid+'\')" ><span class="glyphicon glyphicon-ok"></span> Valider ces dates</button></p>';
	t += '</div>';
	return t;
}


function affBarreLes(ymd, oid)	/* Affiche de la sélection de date à valider */
{
	var _ = date_help_write_data[oid];
	var sentence = ymd;
	if (_.dE_A) { sentence += ' ' + _.dE_A + ' ' + _.heurEsminutes + _.heurEsminutEsEtDe; }

	var t = '<div class="input-group">';
	t += '<input class="form-control" type="text" name="showPartSentence" id="'+oid+'showPartSentence" readonly="true" value="'+sentence+'">';
	t += '<span class="input-group-btn"><button type="button" name="Valider" class="btn btn-primary" onclick="ajoutTab(\''+oid+'\')" ><span class="glyphicon glyphicon-plus"></span>Ajouter à la liste</button></span></div>';

	return t;

}


function afficherListe(oid)	/* Création de la liste à afficher */
{
	var _ = date_help_write_data[oid];
	var listeDates = $('#'+oid+'listeDates');
	listeDates.html('');

	for (var i = 0; i < _.tab.length; i++)
	{
		if (_.tab[i])
		{
			listeDates.append('<div class="date-item">'+_.tab[i]+'<button type="button" data-index="'+i+'" class="pull-right btn btn-danger btn-xs remove-date" onclick="Supprimer(\''+oid+'\', this);"><span class="glyphicon glyphicon-trash"></span> Supprimer</button></div>');
		}
	};
}

function resetTabLes(oid)
{
	var _ = date_help_write_data[oid];
	_.tab = [];
	_.index = 0;
}

function ajoutTab(oid)
{
	var _ = date_help_write_data[oid];
	var inputDate = document.getElementById(oid+'showPartSentence');
	for (var i = 0; i < _.tab.length; i++)
	{
		if (_.tab[i] == inputDate.value)
		{
			alert("Vous avez déjà sélectionné cette date !");
			return;
		}
	}

	_.tab[_.index] = inputDate.value;
	_.index += 1;
	/*inputDate.value = '';*/
	_.choIxdate = false;
	resetAffichage(oid);
	document.getElementById(oid+"choixADe").innerHTML = buildADe(oid);
	// actualisation du <div>
	var liste = ajoutDatesLes(oid);
	document.getElementById(oid+"ListeDesDates").innerHTML = liste;
    remove_selected(oid);
	afficherListe(oid);

}


function remove_selected(oid){
   $('#'+oid+"SortirCalendar td.selected").removeClass('selected');
}



function Supprimer(oid, element)
{
	var _ = date_help_write_data[oid];
	var selectedIndex = parseInt($(element).data('index'));

	if (selectedIndex >= 0)
	{
		_.tab.splice(selectedIndex,1);
		_.index -= 1;
		$($(this).parents('.date-item').first()).remove();
		afficherListe(oid);

	}
	
}



function joinHours(pDateHours)
{
	var s = '';
	for (var l = 3; l < pDateHours.length; l++) {
		s += ' ' + pDateHours[l]; // copy hours
	}
	return s;
}

function generatePartOfSentence(group, withYear, oid)
{
	var _ = date_help_write_data[oid];
	var val = '';
	if (group.length == 1) {
		val = 'le ' + group[0][_.DAY] + ' ' + group[0][_.MONTH];
		if (withYear) { val += ' ' + group[0][_.YEAR]; }
		val += joinHours(group[0]);
	} else {
		val = 'les ' + group[0][_.DAY];
		val += joinHours(group[0]);
		for (var j = 1; j < group.length-1; j++)
		{
			val += ', ' + group[j][_.DAY];
			val += joinHours(group[j]);
		}
		val += ' et ' + group[group.length-1][_.DAY] + ' ' + group[group.length-1][_.MONTH];
		if (withYear) { val += ' ' + group[0][_.YEAR]; }
		val += joinHours(group[group.length-1]);
	}
	return val;
}

function generateLesSentence(oid)
{
	var _ = date_help_write_data[oid];
	if (_.tab.length === 0)
	{
		document.getElementById(oid).value = '';
		return;
	}
	
	if (_.tab.length == 1)
	{
		document.getElementById(oid).value = 'Le ' + _.tab;
		return;
	}

	var s = [];
	var s_index = 0;
	var lDateTable = _.tab[0].split(" ");
	// initialize group array
	var current_month = lDateTable[_.MONTH];
	var current_year = lDateTable[_.YEAR];
	var group = [];
	var index = 0;
	group[index] = lDateTable;
	index += 1;

	var end_of_tab = false;
	var change_month = false;
	var cur_year = _.todaydate.getFullYear();
	var withYear = cur_year != current_year;
    var val, i;
	for (i = 1; i < _.tab.length; i++)
	{
		lDateTable = _.tab[i].split(" ");
		if ((current_month == lDateTable[_.MONTH]) && (current_year == lDateTable[_.YEAR])) {
			group[index] = lDateTable;
			index += 1;
		} else { // flush the group
			change_month = true;
		}
		if (i == (_.tab.length-1)) { // end of the tab
			end_of_tab = true;
		}
		if (change_month) {
			if (current_year != lDateTable[_.YEAR]) { withYear = true; }
			val = generatePartOfSentence(group, withYear, oid);
			//alert('change_month: '+val);
			s[s_index] = val;
			s_index += 1;
			// reinitialize group array
			current_month = lDateTable[_.MONTH];
			current_year = lDateTable[_.YEAR];
			group = [];
			index = 0;
			group[index] = lDateTable;
			index += 1;
			change_month = false;
		}
		if (end_of_tab) {
			val = generatePartOfSentence(group, withYear, oid);
			//alert('endoftab: '+val);
			s[s_index] = val;
			s_index += 1;
		}
	}
	var result = '';
	result = 'L' + s[0].substring(1);
	if (s.length > 1) {
		for (i = 1; i < s.length-1; i++) {
			result += ', ' + s[i];
		}
		result += ' et ' + s[s.length-1];
	}
	document.getElementById(oid).value = result;
}
/* end functions for "Les" mode */


function laDate(ymd, oid)
{
	var _ = date_help_write_data[oid];
	_.choIxdate = true;
	_.ymdc = ymd;
	if (_.choIxmode == 1)
	{
		affResultatLe(ymd, oid);  // conception de la zone text
	}
	if (_.choIxmode == 2)
	{
		var inputDate = affBarreLes(ymd, oid);
		document.getElementById(oid+"messageValidation").innerHTML = inputDate;
	}
	if (_.choIxmode == 3)
	{
		if (!_.choIxDu)
		{
			affBarreDu(ymd, oid);
		}
		else
		{
			affBarreAu(ymd, oid);
		}
	}
	if (_.choIxmode == 4)
	{
		affResultatJusquAu(ymd, oid);  // conception de la zone text 
	}
}



/***********************************************
* Basic Calendar-By Brian Gosselin at http://scriptasylum.com/bgaudiodr/
* Script featured on Dynamic Drive (http://www.dynamicdrive.com)
* This notice must stay intact for use
* Visit http://www.dynamicdrive.com/ for full source code
***********************************************/

/* This script have been translated in french and slightly modified
for SortirWeekend portal by Vincent Fretin */

function buildCal(m, y, oid)
{
 var _ = date_help_write_data[oid];
 var mn =['Janvier','F&eacute;vrier','Mars','Avril','Mai','Juin','Juillet','Ao&ucirc;t','Septembre','Octobre','Novembre','D&eacute;cembre'];
 var mns=['janvier','f&eacute;vrier','mars','avril','mai','juin','juillet','ao&ucirc;t','septembre','octobre','novembre','d&eacute;cembre'];
 var dim=[31,0,31,30,31,30,31,31,30,31,30,31];

  var oD = new Date(y, m-1, 1);
/*  oD.od=oD.getDay()+1;*/
  oD.od=oD.getDay();
  if (oD.od === 0) 
  {
     oD.od=7;
  }

  var todaydate=new Date();

  var scanfortoday=(y==todaydate.getFullYear() && m==todaydate.getMonth()+1)? todaydate.getDate() : 0;

  dim[1]=(((oD.getFullYear()%100!==0)&&(oD.getFullYear()%4===0))||(oD.getFullYear()%400===0))?29:28;

  var t='<table>\n<thead><tr>\n';
  t+='<td class="SortirCalendar_previous_month"><a href="javascript:previousMonth(\''+oid+'\')" title="Mois pr&eacute;c&eacute;dent">&lt;&lt;</a></td>\n';
  t+='<td colspan="5" class="SortirCalendar_month_year">'+mn[m-1]+' '+y+'</td>\n';
  t+='<td class="SortirCalendar_next_month"><a href="javascript:nextMonth(\''+oid+'\')" title="Mois suivant">&gt;&gt;</a></td>\n';
  t+='</tr>\n<tr>\n';


  var dow=['Lu','Ma','Me','Je','Ve','Sa','Di'];

  for (s=0;s<7;s++) 
  {
    t+='<th>'+dow[s]+'</th>\n';
  }

  t+='</tr>\n</thead>\n<tbody>\n<tr>\n';  
  var end=42;
  if ((dim[m-1]+oD.od-1) <= 35)
  {
    end=35;
  }

  for (i=1;i<=end;i++)
  {
    var x=((i-oD.od>=0)&&(i-oD.od<dim[m-1]))? i-oD.od+1 : '&nbsp;';
    if (x==scanfortoday) 
    {
      x='<span class="SortirCalendar_today">'+x+'</span>';
    }

/*
    now = new Date();
    now.setTime(Date.parse(m+'/'+(i-oD.od+1)+'/'+y))
    var jIn = now.toString().substring(0,3);
    var jOut = '' 
    if(jIn=="Mon"){ jOut="lundi"; }
    if(jIn=="Tue"){ jOut="mardi"; }
    if(jIn=="Wed"){ jOut="mercredi"; }
    if(jIn=="Thu"){ jOut="jeudi"; }
    if(jIn=="Fri"){ jOut="vendredi"; }
    if(jIn=="Sat"){ jOut="samedi"; }
    if(jIn=="Sun"){ jOut="dimanche"; }
    var ymd = jOut+'&nbsp;'+(i-oD.od+1)+'&nbsp;'+mns[_.curmonth-1] +'&nbsp;'+ _.curyear;
*/
    var day = (i-oD.od+1);
    if (day == 1) { day = '1er'; }
    var ymd = day + ' ' + mns[m-1] + ' ' + y;

    if (x=='&nbsp;') 
    {
      t+='<td></td>\n';
    } 
    else 
    {
       if (_.choixmode === '') // si on a pas encore selectionné de mode, on n'active pas les liens
       {
         t+='<td>'+x+'</td>\n';
       }
       else
       {
         t+="<td class=\"calendar-date\" onclick=\"javascript:laDate('"+ymd+"','"+oid+"');remove_selected('"+oid+"'); $(this).addClass('selected');return false;\">"+x+"</td>\n";
       }
    }

    if(((i)%7===0)&&(i<=(end-7))) {
        t+='</tr>\n<tr>\n';
    }
  }
  t+='</tbody>\n</tr>\n</table>\n';
  return t;
}

function previousMonth(oid)
{
  var _ = date_help_write_data[oid];
  if (_.curmonth == 1) 
  {
    _.curyear--;
    _.curmonth=12;
  }
  else
  {
    _.curmonth--;
  }
  var newCalendar = buildCal(_.curmonth,_.curyear,oid);
  document.getElementById(oid+"SortirCalendar").innerHTML=newCalendar;
}

function nextMonth(oid) 
{
  var _ = date_help_write_data[oid];
  if (_.curmonth == 12) {
    _.curyear++;
    _.curmonth=1;
  } 
  else 
  {
    _.curmonth++;
  }
  var newCalendar = buildCal(_.curmonth,_.curyear,oid);
  document.getElementById(oid+"SortirCalendar").innerHTML=newCalendar;
}


function init_date_ical(date_input){
	var oid = $(date_input).attr('id');
	init_date_help_data(oid);
	//document.getElementById(oid+"SortirCalendar").innerHTML = buildCal(_.curmonth,_.curyear,oid);
	$($(date_input).parents('.input-group').first().find('.btn.help-activator').first()).on('click', function(){
		var widgt = $($(this).parents('.help-date-wdget').first().find('.helpWriteSeances').first());
		  if($(this).hasClass('closed')){
		    widgt.slideDown( );
		    widgt.removeClass('hide-bloc');
		    $(this).removeClass('closed');
		    $(this).addClass('active');

		  }else{
		    widgt.slideUp( );
		    widgt.addClass('hide-bloc');
		    $(this).removeClass('active');
		    $(this).addClass('closed');
		  }
	})
};

$(document).ready(function(){
	var dates = $('.form-control-date');
	for(var i=0; i<dates.length; i++){
		init_date_ical(dates[i])
	}
});
