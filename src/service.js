import axios from "axios";
import { serverBasedURL } from "./utils";

class TitleGenService {
    constructor() {
        this.apiURL = serverBasedURL
    }

    async autoComplete( prefix ) { 
        const response = await axios.post(this.apiURL +"/complete/", prefix)
        .catch( error => {
            throw error
        }) 
        return response
    }

}

export default new TitleGenService()