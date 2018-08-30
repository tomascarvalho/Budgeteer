
function addExpense (event)
{
    //console.log("addExpense was called");
    //event.preventDefault();
    var ammount = document.getElementById("ammount").value;
    var description = document.getElementById("description").value;
    var account = document.getElementById("account").value;
    var date = document.getElementById("date").value;

    console.log(isValidDate(date));
    if (isValidDate(date) == null)
    {
        alert("Invalid date input! Use format yyyy-MM-dd");
        return;
    }
    if (!isValidNumber(ammount))
    {
        alert("Invalid ammount input!");
        return;
    }


    var rows = "";
    if (ammount > 0)
    {
        rows += "<td class = \"positive\">+" + ammount + "€</td><td>" + account + "</td><td>" + description + "</td><td>" + date + "</td>";
    }
    else if (ammount < 0)
    {
        rows += "<td class = \"negative\">" + ammount + "€</td><td>" + account + "</td><td>" + description + "</td><td>" + date + "</td>";
    }
    else
        rows += "<td>" + ammount + "</td><td>" + account + "</td><td>" + description + "</td><td>" + date + "</td>";
    var tbody = document.querySelector("#tableDashboard tbody");
    var tr = document.createElement("tr");

    tr.innerHTML = rows;
    tbody.appendChild(tr);
}

function addAccount(event)
{
    console.log("addAccount was called...");
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1; //January is 0!
    var yyyy = today.getFullYear();

    if(dd<10) {
        dd='0'+dd
    }

    if(mm<10) {
        mm='0'+mm
    }

    today = yyyy+'-'+mm+'-'+dd;
    var name = document.getElementById("name").value;
    var description = document.getElementById("description").value;
    var balance = document.getElementById("balance").value;
    var rows = "";
    if (!isValidNumber(balance))
    {
        alert("Invalid ammount input!");
        return;
    }

    if (balance > 0)
    {
        rows += "<td class = \"tdManagement\">" + name + "</td><td class = \"tdManagement\">" + description + "</td><td class = \"tdManagement positive\">" + balance + "€</td><td class = \"tdManagement\">" + today + "</td>";
    }
    else if (balance < 0)
    {
        rows += "<td class = \"tdManagement\">" + name + "</td><td class = \"tdManagement\">" + description + "</td><td class = \"tdManagement negative\">" + balance + "€</td><td class = \"tdManagement\">" + today + "</td>";
    }
    else
        rows += "<td class = \"tdManagement\">" + name + "€</td><td class = \"tdManagement\">" + description + "</td><td class = \"tdManagement\">" + balance + "</td><td class = \"tdManagement\">" + today + "</td>";
    var tbody = document.querySelector("#tableAccManagement tbody");
    var tr = document.createElement("tr");

    tr.innerHTML = rows;
    tbody.appendChild(tr);

}


function isValidDate(dateString) {
    var regEx_A = /^(19|20)\d\d[- \/.](0[1-9]|1[012])[- \/.](0[1-9]|[12][0-9]|3[01])$/;
    var regEx_B = /^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$/;
    console.log(dateString);
    if (dateString.match(regEx_A) == null)
    {
        if (dateString.match(regEx_B) == null)
            return null;
    }
    return true;
}

function isValidMail (emailString)
{
    var regEx = /.+@.+/;
    return (emailString.match(regEx) != null);
}

function isValidNumber (numberString) {
    var regEx = /^[-+]?[0-9]*(\.|\,)?[0-9]{1,2}$/;
    return (numberString.match(regEx) != null);
}

function responseHandler(event)
{
    window.alert(this.responseText);
}

function warnUser(event)
{
    console.log("Triggered");
    event.returnValue = "warning!";
    return "warning!";
}

if (document.body.id == "logIn")
{
    document.getElementById("log_in").addEventListener("click", function(event)
    {
        console.log("Entra");
        var email = document.getElementById("email").value;
        if (!isValidMail(email) || email == "")
        {
            alert("Invalid Email!");
            event.preventDefault();
            return;
        }
        else if (document.getElementById("password").value == "")
        {
            alert("Fill Password Field!");
            event.preventDefault();
            return;
        }
    });
}

if (document.body.id == "manageAccounts" || document.body.id == "manageObjectives")
{
    document.getElementById("editRow").addEventListener("click", function()
    {
        var i = 1;
        var current = document.getElementById("editRow");
        var row_col = "";
        row_col += "row" + current.value + "_col";
        for (i = 1; i <= 3; i++)
        {
            if (current.innerHTML == "Edit")
                document.getElementById(row_col+""+i).setAttribute('contenteditable', "true");
            if (current.innerHTML == "Save")
                document.getElementById(row_col+""+i).setAttribute('contenteditable', "false");
        }
        if (current.innerHTML == "Save")
        {
            current.innerHTML = "Edit";
        }
        else if (current.innerHTML == 'Edit'){
            current.innerHTML = "Save";
        }

    });



    document.getElementById("editRow2").addEventListener("click", function()
    {
        var i = 1;
        var current = document.getElementById("editRow2");
        var row_col = "";
        row_col += "row" + current.value + "_col";
        for (i = 1; i <= 3; i++)
        {
            if (current.innerHTML == "Edit")
                document.getElementById(row_col+""+i).setAttribute('contenteditable', "true");
            if (current.innerHTML == "Save")
                document.getElementById(row_col+""+i).setAttribute('contenteditable', "false");
        }
        if (current.innerHTML == "Save")
        {
            current.innerHTML = "Edit";
        }
        else if (current.innerHTML == 'Edit'){
            current.innerHTML = "Save";
        }

    });

    document.getElementById("editRow3").addEventListener("click", function()
    {
        console.log("Entra ao menos");
        var i = 1;
        var current = document.getElementById("editRow3");
        var row_col = "";
        row_col += "row" + current.value + "_col";
        for (i = 1; i <= 3; i++)
        {
            if (current.innerHTML == "Edit")
                document.getElementById(row_col+""+i).setAttribute('contenteditable', "true");
            if (current.innerHTML == "Save")
                document.getElementById(row_col+""+i).setAttribute('contenteditable', "false");
        }
        if (current.innerHTML == "Save")
        {
            current.innerHTML = "Edit";
        }
        else if (current.innerHTML == 'Edit'){
            current.innerHTML = "Save";
        }

    });

}

if (document.body.id == "manageObjectives")
{

    document.getElementById("addObjectiveButton").addEventListener("click", function(event)
    {
        var name = document.getElementById("name").value;
        if (name == "")
        {
            alert("Choose a name for your objective");
            return;
        }
        var amount = document.getElementById("amount").value;
        if (!isValidNumber(amount))
        {
            console.log(amount);
            alert("Invalid amount");
            return;
        }
        var option = document.getElementById("option").value;
        var date = document.getElementById("date").value;
        if (!isValidDate(date))
        {
            alert("Invalid date! Use format: yyyy-MM-dd");
            return;
        }
        var account = document.getElementById("account").value;
        var rows = "";

        rows += "<td class = \"tdManagement\">" + name + "</td><td class = \"tdManagement\">" + option + " " + amount + "€ from " + account + "</td><td class = \"tdManagement\">" + date + "</td>";
        var tbody = document.querySelector("#tableObjManagement tbody");
        var tr = document.createElement("tr");

        tr.innerHTML = rows;
        tbody.appendChild(tr);

    });
}
if (document.body.id == "signUp")
{
    document.getElementById("submit").addEventListener("click", function(event)
    {
        var email = document.getElementById("email").value;
        if (!isValidMail(email))
        {
            alert("Invalid Email!");
            event.preventDefault();
            return;
        }
        if (document.getElementById("password").value != document.getElementById("confirm_password").value)
        {
            alert("Password doesn't match!");
            event.preventDefault();
            return;
        }
        else if (document.getElementById("password").value == "")
        {
            alert("Fill Password Field!");
            event.preventDefault();
            return;
        }

    });
}
