import axios from "axios";
class TitleGenService {
    constructor() {
        this.apiURL = "http://localhost:3000/"
    }

    async autoComplete( prefix ) { 

        const response = await axios.post(this.apiURL +"api/autocomplete/", prefix)
        .catch( error => {
            throw error
        }) 
        return response
    }

}

export default new TitleGenService()