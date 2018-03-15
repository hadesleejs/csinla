function sendRentingType(){
	var type = document.getElementsByName("type");
	for(var i=0;i<type.length;i++)
	{
		if(type[i].checked)
		{
			truetype = type[i].value;
		}
	}

	var locat = document.getElementsByName("location");
	for(var i=0;i<locat.length;i++)
	{
		if(locat[i].checked)
		{
			trueloc = locat[i].value;
			// alert(trueloc)
		}
	}

	var price = document.getElementsByName("price");
	for(var i = 0;i<price.length;i++)
	{
		if(price[i].checked)
		{
			trueprice = price[i].value;
		}
	}

    location.href = "/posts/listRent?type="+truetype+"&locat="+trueloc+"&price="+trueprice
}

function sendRentingType2(){
	var type = document.getElementsByName("mtype");
	for(var i=0;i<type.length;i++)
	{
		if(type[i].checked)
		{
			truetype = type[i].value;
		}
	}

	var locat = document.getElementsByName("mlocation");
	for(var i=0;i<locat.length;i++)
	{
		if(locat[i].checked)
		{
			trueloc = locat[i].value;
			// alert(trueloc)
		}
	}

	var price = document.getElementsByName("mprice");
	for(var i = 0;i<price.length;i++)
	{
		if(price[i].checked)
		{
			trueprice = price[i].value;
		}
	}

    location.href = "/posts/listRent?type="+truetype+"&locat="+trueloc+"&price="+trueprice
}

function sendCarType(){
	var type = document.getElementsByName("type");
	for(var i=0;i<type.length;i++)
	{
		if(type[i].checked)
		{
			truetype = type[i].value;
		}
	}

	var level = document.getElementsByName("level");
	for(var i=0;i<level.length;i++)
	{
		if(level[i].checked)
		{
			truelev = level[i].value;
			// alert(trueloc)
		}
	}

	var transmission = document.getElementsByName("transmission");
	for(var i = 0;i<transmission.length;i++)
	{
		if(transmission[i].checked)
		{
			truetrans = transmission[i].value;
		}
	}

	var price = document.getElementsByName("price");
	for(var i = 0;i<price.length;i++)
	{
		if(price[i].checked)
		{
			trueprice = price[i].value;
		}
	}

    location.href = "/posts/Car?type="+truetype+"&level="+truelev+"&transmission="+truetrans//+"&price="+trueprice
}
