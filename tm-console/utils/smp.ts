const setHeight = () => {
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
}

const invalidHover = () => {
    addEventListener('DOMContentLoaded', function(){
        if( isTouchDevice() ){
            for( var i in document.styleSheets ) if( document.styleSheets.hasOwnProperty(i) ){
                deleteRuleHover(document.styleSheets[i]);
            }
        }
        function isTouchDevice() {
            return 'ontouchstart' in document.documentElement || navigator.maxTouchPoints || (navigator as any).msMaxTouchPoints;
        }
        function deleteRuleHover( styleSheet: any){
            try{
                var rules = styleSheet.cssRules || styleSheet.rules;
                if( rules ){
                    for( var i=rules.length; i--; ){
                        var text = rules[i].selectorText;
                        if( /:hover/.test(text) ){
                            //console.log(text);
                            styleSheet.deleteRule(i);
                        }
                    }
                    for( var i=rules.length; i--; ) deleteRuleHover(rules[i]);
                }
            }
            catch(ex){
                //console.log(ex);
            }
        }
    });
}

export { setHeight, invalidHover };