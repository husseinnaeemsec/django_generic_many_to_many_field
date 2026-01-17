function capitalizeWords(str) {
  return str
    .split(" ")
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

function getValues(){
    const rawValue = document.getElementById("_dynamic_json_field_widget_value");
    if(rawValue){
        try{
            return JSON.parse(rawValue.textContent);
        }catch{
            return null
        }
    }
    return null
}

document.addEventListener("DOMContentLoaded",(e)=>{
    const rawWidgetData = document.getElementById('_dynamic_json_field_widget_data');
    try{
        const widgetData = JSON.parse(rawWidgetData.textContent);
        const {attrs,name} = widgetData;
        const widget_menu = document.getElementById("_dynamic_json_field_container")
        const {content_type_field,choices_endpoint} = attrs;
        const contentTypeSelectMenu = document.querySelector(`[name="${content_type_field}"]`);
        handleContentTypeChange(contentTypeSelectMenu,choices_endpoint,widget_menu,name)
        contentTypeSelectMenu.addEventListener("change",(e)=>{
            handleContentTypeChange(e.target,choices_endpoint,widget_menu,name);
        })
    }catch{
        console.error(`Failed initializing dynamic many-to-many widget `)
    }
})

async function handleContentTypeChange(menu,choices_endpoint,widget_menu,widget_name){
    const {value} = menu;
    const instanceValue = getValues()
    widget_menu.innerHTML = '';
    widget_menu.innerHTML = '<p class=" p-2 text-slate-500"> Please wait while loading instances </p>'
    if(value && !isNaN(value)){
        fetch(
            choices_endpoint,
            {
                method:"POST",
                headers:{
                    "Content-Type":'application/json',
                    "X-Requested-With":"XMLHttpRequest"
                },
                body:JSON.stringify({
                    'content_type_id': value
                })
            }
        )
        .then((res)=> res.json())
        .then((data)=>{
            widget_menu.innerHTML = ''
            if(data?.length){
                data.forEach(item => {

                    widget_menu.appendChild(
                        createCheckboxItem(widget_name,item,instanceValue)
                    );
                })
            }
        })
        .catch((e)=>{
            widget_menu.innerHTML = '<p class=" p-2 text-red-500"> Failed to load instances </p>'  
        })
    }else{
        const placeholder = document.createElement("p");
        placeholder.className = " p-2 text-slate-500";
        placeholder.textContent = `Select ${capitalizeWords(menu.name.replace("_"," "))}`;
        placeholder.addEventListener("click",(e)=>{
            menu.focus()
        })
        widget_menu.innerHTML = ''
        widget_menu.appendChild(placeholder);
    }
}

function createCheckboxItem(field_name,item,instanceValue){
    const container = document.createElement("div");
    container.className = 'model-choice-container';
    const label = document.createElement("label");
    label.textContent = item.str;
    const checkbox = document.createElement("input");
    checkbox.type = 'checkbox';
    checkbox.value = item.id
    checkbox.name = field_name;
    if(instanceValue && Array.isArray(instanceValue) && instanceValue.length && instanceValue.includes(item.id)){
        checkbox.checked = true;
    }
    container.appendChild(checkbox);
    container.appendChild(label);
    return container
}