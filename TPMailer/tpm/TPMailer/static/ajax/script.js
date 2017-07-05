$(document).ready(function()
{
    $('#dash').click(function()
    {
        alert('dash')
    })

    $('#dash_confs').click(function()
    {
        alert('dash_confs')
        $('#ContentHeader').load('TPMailer/dashboard.html', {'T': True});
    })

    $('#dash_users').click(function()
    {
        alert('dash_users')
        // HTML manipulations
    })

    $('#dash_settings').click(function()
    {
        alert('dash_settings')
        // HTML manipulations
    })
})