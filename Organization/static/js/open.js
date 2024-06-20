
var $j = jQuery.noConflict();

$j(document).ready(function () {
    $j(".open-popup").click(function () {
        var serialNo = $j(this).closest("tr").find("td:eq(0)").text();
        var donorName = $j(this).closest("tr").find("td:eq(1)").text();
        var amount = $j(this).closest("tr").find("td:eq(2)").text();
        var date = $j(this).closest("tr").find("td:eq(3)").text();
        var message = $j(this).data("message");

        $j("#popupSerialNo").text(serialNo);
        $j("#popupDonorName").text(donorName);
        $j("#popupAmount").text(amount);
        $j("#popupDate").text(date);
        $j("#popupMessage").text(message);

        $j("#myPopup").modal();
    });

    // Your other jQuery code can be placed here using $j instead of $
});
