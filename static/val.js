function validation()
        {
            var a=document.getElementById("a1").value;
            if (a=="")
            {
                window.alert("name must be filled")
                focus.a;
                return false;
            }
            var b=document.getElementById("a2").value;
            if (b=="")
            {
                window.alert("username must be filled")
                focus.b;
                return false;
            }
            var c=document.getElementById("a3").value;
            if (c=="")
            {
                window.alert("email must be filled")
                focus.c;
                return false;
            }
            var d=document.getElementById("a4").value;
            if (d=="")
            {
                window.alert("phone number must be filled")
                focus.d;
                return false;
            }
            var d1=document.getElementById("a4").value;
            if (d1.length!=10)
            {
                window.alert("phone number must have 10 digits")
                focus.d1;
                return false;
            }
            var e=document.getElementById("a5").value;
            if (e=="")
            {
                window.alert("password must be filled")
                focus.e;
                return false;
            }
            var e1=document.getElementById("a5").value;
            if (e1.length<8)
            {
                window.alert("password at least have 8 letters")
                focus.e1;
                return false;
            }
            var f=document.getElementById("a6").value;
            if (f=="")
            {
                window.alert("password must confirm")
                focus.f;
                return false;
            }
            var f1=document.getElementById("a5").value;
            var f2=document.getElementById("a6").value;
            if (f1!=f2)
            {
                window.alert("password does not match")
                return false;
            }
        }












