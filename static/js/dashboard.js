heroes = new Array();
heroes[1] = "Antimage";
heroes[2] = "Axe";
heroes[3] = "Bane";
heroes[4] = "Bloodseeker";
heroes[5] = "Crystal Maiden";
heroes[6] = "Drow Ranger";
heroes[7] = "Earthshaker";
heroes[8] = "Juggernaut";
heroes[9] = "Mirana";
heroes[10] = "Morphling";
heroes[11] = "Nevermore";
heroes[12] = "Phantom Lancer";
heroes[13] = "Puck";
heroes[14] = "Pudge";
heroes[15] = "Razor";
heroes[16] = "Sand King";
heroes[17] = "Storm Spirit";
heroes[18] = "Sven";
heroes[19] = "Tiny";
heroes[20] = "Vengefulspirit";
heroes[21] = "Windrunner";
heroes[22] = "Zuus";
heroes[23] = "Kunkka";
heroes[25] = "Lina";
heroes[26] = "Lion";
heroes[27] = "Shadow Shaman";
heroes[28] = "Slardar";
heroes[29] = "Tidehunter";
heroes[30] = "Witch Doctor";
heroes[31] = "Lich";
heroes[32] = "Riki";
heroes[33] = "Enigma";
heroes[34] = "Tinker";
heroes[35] = "Sniper";
heroes[36] = "Necrolyte";
heroes[37] = "Warlock";
heroes[38] = "Beastmaster";
heroes[39] = "Queenofpain";
heroes[40] = "Venomancer";
heroes[41] = "Faceless Void";
heroes[42] = "Skeleton King";
heroes[43] = "Death Prophet";
heroes[44] = "Phantom Assassin";
heroes[45] = "Pugna";
heroes[46] = "Templar Assassin";
heroes[47] = "Viper";
heroes[48] = "Luna";
heroes[49] = "Dragon Knight";
heroes[50] = "Dazzle";
heroes[51] = "Rattletrap";
heroes[52] = "Leshrac";
heroes[53] = "Furion";
heroes[54] = "Life Stealer";
heroes[55] = "Dark Seer";
heroes[56] = "Clinkz";
heroes[57] = "Omniknight";
heroes[58] = "Enchantress";
heroes[59] = "Huskar";
heroes[60] = "Night Stalker";
heroes[61] = "Broodmother";
heroes[62] = "Bounty Hunter";
heroes[63] = "Weaver";
heroes[64] = "Jakiro";
heroes[65] = "Batrider";
heroes[66] = "Chen";
heroes[67] = "Spectre";
heroes[68] = "Ancient Apparition";
heroes[69] = "Doom Bringer";
heroes[70] = "Ursa";
heroes[71] = "Spirit Breaker";
heroes[72] = "Gyrocopter";
heroes[73] = "Alchemist";
heroes[74] = "Invoker";
heroes[75] = "Silencer";
heroes[76] = "Obsidian Destroyer";
heroes[77] = "Lycan";
heroes[78] = "Brewmaster";
heroes[79] = "Shadow Demon";
heroes[80] = "Lone Druid";
heroes[81] = "Chaos Knight";
heroes[82] = "Meepo";
heroes[83] = "Treant";
heroes[84] = "Ogre Magi";
heroes[85] = "Undying";
heroes[86] = "Rubick";
heroes[87] = "Disruptor";
heroes[88] = "Nyx Assassin";
heroes[89] = "Naga Siren";
heroes[90] = "Keeper Of The Light";
heroes[91] = "Wisp";
heroes[92] = "Visage";
heroes[93] = "Slark";
heroes[94] = "Medusa";
heroes[95] = "Troll Warlord";
heroes[96] = "Centaur";
heroes[97] = "Magnataur";
heroes[98] = "Shredder";
heroes[99] = "Bristleback";
heroes[100] = "Tusk";
heroes[101] = "Skywrath Mage";
heroes[102] = "Abaddon";
heroes[103] = "Elder Titan";
heroes[104] = "Legion Commander";
heroes[106] = "Ember Spirit";
heroes[107] = "Earth Spirit";
heroes[109] = "Terrorblade";
heroes[110] = "Phoenix";
var service = '1';
function adjust_selector() {
    $('#hero_selector').css('width', Math.floor($(window).width() * 0.9 / 137) * 137);
}
$(window).resize(adjust_selector);
adjust_selector();
var active_class = "#strength";
function enable_filter(nclass) {
    $(active_class + '_class').hide();
    $(active_class + '_filter').removeClass('active');
    active_class = nclass
    $(active_class + '_class').show();
    $(active_class + '_filter').addClass('active');
    return false;
}
$('#strength_filter').click(function() { return enable_filter('#strength'); });
$('#agility_filter').click(function() { return enable_filter('#agility'); });
$('#intelligence_filter').click(function() { return enable_filter('#intelligence'); });
$('#strength_filter').trigger('click');

$('.avatar').each(function(index) {
    $(this).click(function() {
	    var heroid = $(this).attr('id').substring(12);
	    $('#hero_indicator').html(heroes[parseInt(heroid)]);
        $('#toggle_selector').css('display', 'none');
        $('.steady').css('opacity', 1);
        $('#match_data_div').html('<div style="text-align:center"><img src="/dotalight/static/img/in-progress.gif" class="progress-img"><br>Loading...</div>');
        $('.navbar-collapse').collapse('hide');
        $.post('', {service: service, heroid: heroid})
         .done(function(data) {
	         $('#match_data_div').html(data);
        });
    });
    $(this).mousedown(function() {$(this).css('border-color', '#0f0');});
    $(this).mouseup(function() {$(this).css('border-color', '#333');});
    $(this).mouseleave(function() {$(this).css('border-color', '#333');});
});
$('#select_all_heroes').click(function () {
    $('#hero_indicator').html("All Heroes");
    $('#match_data_div').html('<div style="text-align:center"><img src="/dotalight/static/img/in-progress.gif" class="progress-img"><br>Loading...</div>');
    $('.navbar-collapse').collapse('hide');
    $.post('', {service: service})
     .done(function(data) {
	     $('#match_data_div').html(data);
    });
});
$('#select_hero').click(function () {
    $('#toggle_selector').css('display', 'block');
    $('.steady').css('opacity', 0.1);
});
$('#view_matches').click(function () {
    service = 1;
    $('#view_matches_li').addClass('active');
    $('#view_trend_li').removeClass('active');
    $('.dropdown-trend-item').removeClass('active');
    $('#hero_indicator').html('All Heroes');
    $('#match_data_div').html('<div style="text-align:center"><img src="/dotalight/static/img/in-progress.gif" class="progress-img"><br>Loading...</div>');
    $('.navbar-collapse').collapse('hide');
    $.post('', {service: service})
     .done(function(data) {
	     $('#match_data_div').html(data);
    });
});
function activate_trend() {
    $('#view_matches_li').removeClass('active');
    $('#view_trend_li').addClass('active');
    $('.dropdown-trend-item').removeClass('active');
    $('#match_data_div').html('<div style="text-align:center"><img src="/dotalight/static/img/in-progress.gif" class="progress-img"><br>Loading...</div>');
    $('.navbar-collapse').collapse('hide');
    $.post('', {service: service})
     .done(function(data) {
	 $('#match_data_div').html(data);
    });
}
$('#view_trend_kda').click(function () {
    service = 2;
    activate_trend();
    $('#view_trend_kda_li').addClass('active');
});
$('#view_trend_lhd').click(function () {
    service = 3;
    activate_trend();
    $('#view_trend_lhd_li').addClass('active');
});
$('#view_trend_ge').click(function () {
    service = 4;
    activate_trend();
    $('#view_trend_ge_li').addClass('active');
});
