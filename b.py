import requests
import json
import time
from datetime import datetime

def scrape_all_reviews():
    # API endpoint and authentication
    api_url = "https://api.apify.com/v2/acts/compass~google-maps-reviews-scraper/run-sync-get-dataset-items"
    token = "apify_api_o7mYRW8cyWa4FtBMQFfhu8rBpfWqVb1AnFwN"

    # Hardcoded place IDs
    place_ids = [
        "ChIJwT1ckb2D0ocRT89CQb1cRZM",
        "ChIJfSQZZc_XzIcRByXoB_a8M3U",
        "ChIJQaXjGj2lJwQR6dRJhq0D3Z4",
        "ChIJWaKeT3C3M4YR1nzImIo3AuY",
        "ChIJmZfiZHPgMoYRx6Jl1TTdKTU",
        "ChIJe0NwW4eFM4YRo2hXq0LSVOI",
        "ChIJr34ZyAUSNIYRftAb91cikQg",
        "ChIJO_NV-KicM4YRSqclbdyVaOQ",
        "ChIJfdpRCmFtNIYR5-Gk7GEQ--0",
        "ChIJPQrnZP9gM4YRFwQrGB1GSAc",
        "ChIJA_P2K9qdNIYRu6uXrL1KVNQ",
        "ChIJM2O8bVu_NIYRB1Dl0oOj9g0",
        "ChIJcw-uvDwONIYRBJ1DBm79TYE",
        "ChIJ87Wwo5J6hIkR7uhFwRDbDI0",
        "ChIJVaccTYi_NIYRDLQJjA_0Cb8",
        "ChIJczC6MiKCoW0R3FAIXgwm8o0",
        "ChIJiZTNf8yuIgwRvMjsM42TByQ",
        "ChIJPzQiXlK1y4cR3pUgna3WVlY",
        "ChIJcckIpce1y4cRY0CZ_ov2R58",
        "ChIJsehamPALT2YRfdEQBtfWkNs",
        "ChIJzRfF3YK3y4cRZk9nSZcivVw",
        "ChIJ_____9tMyocRqyPBQsin3K0",
        "ChIJAQAAAMRMyocRfGQ5yR3-8Rg",
        "ChIJ59aFQK1MyocRf5BYS1cD-Vk",
        "ChIJqUvTkkHGy4cRXBEodnhPVGo",
        "ChIJt7JLaFGyy4cRZ04j7vXnRj8",
        "ChIJAQAAAMRMyocRhsKFb_9iMe8",
        "ChIJAUDzqv-sy4cREQpXHYpHSmc",
        "ChIJhw6TJkuzy4cRvAn2eTzzIhE",
        "ChIJdTBKjCyyy4cRJEQNHWSoqY4",
        "ChIJQ793fc7ry4cRGCeVlUQCBks",
        "ChIJFwSuelwnyocRYjxVccz2TNc",
        "ChIJ6ynF3_IBy4cRTQkSSdxGfD8",
        "ChIJAQAAAMRMyocRlyIoXPTukg4",
        "ChIJgY1BOAlNyocRpkrm9PbpCsY",
        "ChIJV4iUlvPNy4cRXZeNlUup2ms",
        "ChIJ9cQuXTizy4cRMBqrpgsy708",
        "ChIJVSOxjDmzgSIREyW4IgzJ2L8",
        "ChIJVSWvLMYO0UgRh1Vr2xUROGw",
        "ChIJX3crTHu1y4cRf6SGNQMbqTw",
        "ChIJR2Y8vHWmy4cRK_DAwB6GNGA",
        "ChIJVdiloFxbM4YRS8kngxirBXs",
        "ChIJcQ4SPEShgG4RzWy6_sHLrgI",
        "ChIJ8wwKGgt3y4cRgBbURKtYmF8",
        "ChIJrTumsUP-zIcRF8V1224ozlA",
        "ChIJGxO0_GtJyocRyAkOlNPZINU",
        "ChIJ7RvX2GhuyYcRqSyZ8GgXbLM",
        "ChIJEcvoa_NLyYcR8J22wQtK5D0",
        "ChIJFTMo0Bz7ISURzDPV0lb59iA",
        "ChIJYbxZfTlRZmYR9oFrjROcrHk",
        "ChIJhahV745yRG0RHCBesuNAYeQ",
        "ChIJP_Gpjqel0ocRTwh_HPfhboM",
        "ChIJy73ecAtxSmsRQhzlqo9zxiQ",
        "ChIJR8jPxYVLLYYRbgTMb-Ig2Og",
        "ChIJme5fU6MVLYYRg6i5iyITpnE",
        "ChIJVVVVVUWp0ocRWXif5fdDDYk",
        "ChIJa-FxKV87LYYRg6NP8wVJRDM",
        "ChIJ04WkPqh_0ocRhRbatH26X2E",
        "ChIJT-_rfTCC0ocRpadX5VVUkRA",
        "ChIJc8mzIpBl0ocRz0JyE_uduiY",
        "ChIJ9YKECj6G0ocRL3OFlGgcJIc",
        "ChIJG7URbvTq0ocRYA8uo0bovfE",
        "ChIJMyNIJbhf0ocR7onuk5jmM1A",
        "ChIJ21NQN7CZ0ocRp9UvFto_Zio",
        "ChIJ9xYYzYkeGiAR3aCIO73UhGw",
        "ChIJpUG0dPeD0ocRqO6O9-jUy5A",
        "ChIJr5opmLa90ocRVnlUVa78faY",
        "ChIJPYaXhvuB0ocR8iJZXkQulBQ",
        "ChIJw25Rj-LkUm4RWLDVsa9qrhY",
        "ChIJ9Vvm7L9r0ocR_l5q_P26Np8",
        "ChIJDe2lPGPb1IcR1JJOWwi-L0g",
        "ChIJeQlzsfyX04cRYCPfknMuvwM",
        "ChIJseiKNhiT0ocRLcGVf_DLzew",
        "ChIJ4yCFImzw0ocRFd7qvRsOk3g",
        "ChIJDcgnYulG0ocRqevdjmUcZ4U",
        "ChIJG9RdmMyr04cRRD_ULRzPwbo",
        "ChIJUQ4SWrFlzYcRQhBCNoj8u1A",
        "ChIJhWDI-6Dv0ocRQOmp7Kw6c8U",
        "ChIJVQQC9gV1zYcRHoaPejCzLzM",
        "ChIJ0QbIOpqvzYcRNBzXPEfQ9iw",
        "ChIJe6t9VsdTzIcRulILyt8dPaI",
        "ChIJ_____5tTzIcRA-XOM-Zx4U8",
        "ChIJp_78KhSt0ocRik-_L2Ly2gs",
        "ChIJl_rWNwq90ocR73TPqBi_fUg",
        "ChIJhfF885ZF_GoRU5Y5Dhr0cWc",
        "ChIJce2uq7ex0ocRn5c7USZoV6s",
        "ChIJi1NzVIAH04cRWNbceOlVCVk",
        "ChIJY1AfftrTLIYRKcsUr3_U-ww",
        "ChIJbeXUkp0p1IcRX2azFH6OVpQ",
        "ChIJt_9il6n2Mq8R_JJXI1277MI",
        "ChIJkxoTEefq0ocRDv-RCXPG-XA",
        "ChIJPdR79wD1pYARxU-qsBLrU-I",
        "ChIJMVM2MPXq0ocRQD67g-iCzio",
        "ChIJWYsJ_yaj04cRo9g2VcEOeqc",
        "ChIJA7aDnCuk04cRUjCspdtGseQ",
        "ChIJ7XfJdzH-mGURrbZ6COQ15BA",
        "ChIJiZmI5StH0ocRhRzJOFaUaqY",
        "ChIJAQAAADCk0ocRNTPuiEzlhaE",
        "ChIJj-Ng5Tak0ocRvb1kJoGzkIU",
        "ChIJs4YUUe6n0ocRMmUM6sEyo8Y",
        "ChIJAQAAALS90ocRYzsKrbJNikY",
        "ChIJg8wJPTGh0ocRXQU2LfkxE-U",
        "ChIJXwfUmAS90ocRZLDHv8CKtrQ",
        "ChIJ6x6lOZ2j0ocRNvc4Lmx79aA",
        "ChIJ5yg0GGi_0ocRT1CqBMsN7n0",
        "ChIJ756Jniqk0ocRQPKD4rcOgCI",
        "ChIJVSOxjU0VIGkRRzx1BeJ6yZU",
        "ChIJccitxOvH0ocRj4iJ2wg7_NE",
        "ChIJaYBORYcg0ocReXr0lie2WsU",
        "ChIJf05w8lHt0ocR0XAmVsmRups",
        "ChIJ84mPBNHn0ocR2KRXdPz0_eI",
        "ChIJ_____5MrzYcRjqokow5jpT8",
        "ChIJ7WdLMkIlzYcRxqsQUlab4wk",
        "ChIJIXC2QZVTzYcRFMd6QWE9EG8",
        "ChIJA_fpYdgozYcRv_Y2S8ardxY",
        "ChIJrYBkFHn2ai4R3wmqRJk9OnE",
        "ChIJl7ofgQTdEgoR8eCggq-ntqM",
        "ChIJUfFRmZxNzYcR48MMQvHu3RA",
        "ChIJQVuIS4yvzIcRowle2CTbCwI",
        "ChIJU8NrPshFzYcRkgPf_3v036A",
        "ChIJGaPxpuVTzYcRICLIUEsHmzc",
        "ChIJ383bUCMvzYcREJveebRTTcI",
        "ChIJg3W-sojFWY0RcNxbNGfuKH0",
        "ChIJ6SaKjslZzYcRx0zGOiHD4bY",
        "ChIJj4a-qwJXzYcRPbLJxLh-qBY",
        "ChIJ-Zmy791NzYcRfCcQYlMR7_U",
        "ChIJFT_6Xt9TzYcRuO5XyQShNG8",
        "ChIJNyBncJbPRIYRSrvWOEOgNq8",
        "ChIJ1wxBamK_0ocRxnHg4ylj23Q",
        "ChIJI9L42Mpx9wURtytqo-j7XWQ",
        "ChIJk9pYRMq90ocR7ojXOuCM_FA",
        "ChIJifn44XpYzYcRWeKVooKaDZg",
        "ChIJC44lGbbr0ocRIP6VWsv9N7k",
        "ChIJ29j1aZSV0ocRaPQoPBIvWm4",
        "ChIJK9NsNUuv0ocRwV4WvS_rGxw",
        "ChIJSYRA4xwHAIcRxTsViEl6iq0",
        "ChIJLeQhG9d_uKQRaQdjUr1rAXA",
        "ChIJjRiSCG2f0ocRJTtlndQYNUA",
        "ChIJdX1d_ei_0ocRBAwAlCfI6cI",
        "ChIJq3xOXuC80ocR1fZfAC62ndg",
        "ChIJzfmYIva90ocRVfJI7PKdKJ4",
        "ChIJJ-EMmizB0aIR5Vjg3JA2o5U",
        "ChIJf44cdf5J1IcRCC3wRPNJPpQ",
        "ChIJ7y3Q1v3a04cRlF4yafU6hsI",
        "ChIJpXCFPvYLMoYR-yzzXGINst4",
        "ChIJKYvA-b0RzocRgyjMz539Egk",
        "ChIJl8R0U-Aqo0YRjwORR4iQTis",
        "ChIJgb6eKDgf0YcRYGhlJMu_ieM",
        "ChIJ1XTesS_o0YcReFsIf7ITcuo",
        "ChIJsdeBqHHe0YcRbqqRAWFD9c8",
        "ChIJEWCGhlIV0YcRsaQQHYzflwo",
        "ChIJ0ZAesujO0YcR3p9UnFaud38",
        "ChIJVT4EqHwe_SER8XQq9bih768",
        "ChIJ10V04awTEQYRoy6pQfwYgjQ",
        "ChIJwWSemkouQoUR_yBQ7FTQVOc",
        "ChIJ13hzZfGX0ocRFXqxtfRUx9w",
        "ChIJLTIlKdRhWWIR_75-4jyyVdQ",
        "ChIJRYEyeFD-3CgRuU12zJNPrRY",
        "ChIJQWAZxLzb04cRfcbivvlA0JQ",
        "ChIJI6HZBWTb04cRHxJJNyg2A-U",
        "ChIJf8QP9lhvlYURBk2KLeL8mwI",
        "ChIJ762b31H1zocRrzgbk4_4JzI",
        "ChIJZ1hDbo9fzocRy5xwEJu_Opo",
        "ChIJ4Y-BLTjjzocRkQZQjQ4sxaU",
        "ChIJM0pmhTxfzocRS6W7rxhrJc4",
        "ChIJp6w1arF0qGgRih2W5OKHWZ0",
        "ChIJUa3V-p94eC0RSi44Rjd2IpA",
        "ChIJw3XZjMnSzocR8shWy5mt75Q",
        "ChIJyy1bp7ThtYkRZgadj4F3YvM",
        "ChIJBUJ2vKrjtYkRSEGJE9IORG8",
        "ChIJUe3xj1zgg2sRL1crAFN7C6g",
        "ChIJEwzaD0QTAigRFEroGw5ORg4",
        "ChIJtXNdQlU8zocREovDl_OWlWM",
        "ChIJfTFSg8gd0KURgRan6dNI7is",
        "ChIJ1-ZTlACbX4cR-ZTK5PCzjVg",
        "ChIJC4GbXhlBzocRm3Ku9HjIig0",
        "ChIJR20tK18Bz4cRTtlJM5A2bLE",
        "ChIJA1D4USx2S6MR0bPccNMrpw0",
        "ChIJDaHCppbNzocRpBnTJF9IClc",
        "ChIJyYcMsXLZLUYROjIlca2IxyU",
        "ChIJbfNFeIsYSQ4RS43qFmtIBbs",
        "ChIJh0NBU6E5LYYRpe-k8GdWuF0",
        "ChIJpeohpno_LYYR-zrwRSWRkfE",
        "ChIJZb9TDZ5olacRHknk1mouG4E",
        "ChIJLcpQANVSLIYRzAx7hi2D4fY",
        "ChIJSxLukOWnLYYRexKIxUa446U",
        "ChIJY4OGs_MRII0Rjntw67ediNo",
        "ChIJizE6z6ekLYYRf07Pd4e4Des",
        "ChIJWVyUs0BRzYcRE78fLcy0osQ",
        "ChIJY5k40J_JMoYRiw7lALHnlBk",
        "ChIJve2DcN4C7kwRekA80Nk-C_c",
        "ChIJeRHTnQo3LoYRauI83nx1FVc",
        "ChIJr9_ClVAJLIYRdlDyvHZv_dY",
        "ChIJNWLB9I0DLIYRKQUyoojzHvQ",
        "ChIJfQjMOkJxLYYREbT8ySxAMc4",
        "ChIJY8MC2PfSkIgRYYj_DO4FV5E",
        "ChIJIb2TNu9OWIgRa5C4lCnbxL8",
        "ChIJiz7jWhthLIYRLea9uBliLus",
        "ChIJ9S_Q7JXbMoYRWwFTiBvCSx4",
        "ChIJvzpogKxu5UcRdpn9nuj4Rzg",
        "ChIJ05DyHFkrM4YRpALB7Mwv9wE",
        "ChIJQUesSF7dMoYReemgdTC1Ihc",
        "ChIJs98FOy2qy4cRhXAlmDrySOQ",
        "ChIJ2w9XiALfMoYR7a1O6__pWC0",
        "ChIJlaJ6XPxkXAIRNpwsob7tEfs",
        "ChIJx68Htgz4o64R28K5JYsMhnI",
        "ChIJcVGdj-hTzYcRARju9jG9cIo",
        "ChIJx1i65KNRy4cR7MlaKIbkUxQ",
        "ChIJ2XhggTlTzIcR1HYCVViM8PA",
        "ChIJT6vTDTORQgsR3-4APg3Q27Y",
        "ChIJVVUxH0Jg0ocR0HA0d40a-qo",
        "ChIJLw3lGdRkX0gRkqkndwhgauk",
        "ChIJX8Zuk94qzYcR3PnFn00xNe0",
        "ChIJTfO0Kh0rzYcRA5VbE7jk0vY",
        "ChIJz4TdXmZzhYARfmi5YCQ3J1I",
        "ChIJMeIdwv0vM4YRm8j_39mlMH0",
        "ChIJ9RXqaQPXMoYRo-1y5R2OiRk",
        "ChIJSdlcawAnM4YRy0QTgF47BuM",
        "ChIJV2PiCNIvy4cR--ofpIhNfAM",
        "ChIJM0gHHkwry4cR9FvUZTwX2u0",
        "ChIJNWGeWlMKIk8R2oklYtqT7nU",
        "ChIJ266rRvV2rG4RG3tPErb4350",
        "ChIJC6E4YfxvZIQRyUwWMh6zWZU",
        "ChIJ3YUOQG2A1YcRZ252wiPO34k",
        "ChIJJ6gs9jt2f4gRI-cwqfL3jmA",
        "ChIJL_sSws0M8CMRJN8oTvSENOA",
        "ChIJC3_egd51f4gRdpop4oG0td8",
        "ChIJe_6EqVB2f4gR9hHh7RrMyBQ",
        "ChIJacRe0C_PbycRHkUdpwA6BKs",
        "ChIJAQDMtf-41YcRDERIteZ3ULw",
        "ChIJ62SbO17V1IcR5bpAwZ4AHmQ",
        "ChIJvy_Hjv_A1YcR-5yCAZNS9tw",
        "ChIJJWQWGjjV1IcRs6zmrlG_4K8",
        "ChIJfye3CJ7nwokRFUHkFCG3Pq4",
        "ChIJJ4pN0ANZ1IcRnisWybJevsw",
        "ChIJq9hFSg4R8AsR_c-XF5iVsnY",
        "ChIJ69TMBlTL8KARIegcuem-DaM",
        "ChIJnbyKESop1IcRHPUq6nm8P68",
        "ChIJs7AAYjsp1IcRYgIAQJoHKT4",
        "ChIJfcf1YmOj0ocRN52peBKyFYM",
        "ChIJe3tXSCqZ0ocRbFMyhmyOSzk",
        "ChIJ-9wiaeKl0ocRnKRJZGbm8oQ",
        "ChIJB8rUSu9ZzYcRBCDVwtf__SA",
        "ChIJwzgHzMOj0ocRUjT8EnQ9Dg0",
        "ChIJfcg2Lzyl0ocRliNuhD1gUvI",
        "ChIJAzoBqjCh0ocRYOPv2aOKJok",
        "ChIJxbLO2fC90ocRk1IdqhiHVYo",
        "ChIJn9MHVXcpE4gREDVi5sSJy-E",
        "ChIJ931nnoB-1YcRg7GokgVQG5M",
        "ChIJP1UpnzWd1AER96hH8Iy2EhM",
        "ChIJ0wQwGcuMk4cR5cJq3Jd07JY",
        "ChIJW_Afc5oFz4cRyekUqLm3N0M",
        "ChIJg7YJ-ZHwSQsRQuLDAUe7uts",
        "ChIJJ71tE0m4yIcRTNBXgI0aCBA",
        "ChIJJxOfgIIKnEERc8wU9qpmUeM",
        "ChIJmZG77VofyYcRTEKM4BTz5nE",
        "ChIJxwEBjeFrzocRi1RbAMEB1xs",
        "ChIJUQlPpKN5yYcR2nnmBuETj8c",
        "ChIJqcDb0LtuyYcRxzM9t8y_CMI",
        "ChIJJYIObNZuyYcRYr0fxjv8FvQ",
        "ChIJzzIoPxulzIsRQKFp8n6G7gg",
        "ChIJaeuj2BxtyYcRGa4mbRqLBYo",
        "ChIJ2WoEm3UTyYcROF_Hs4hAdig",
        "ChIJC4z8w9MTyYcR0RD2FHg6dGM",
        "ChIJrdCBnjwTyYcRit43i8YIIsI",
        "ChIJ4Zorv14EyYcRHaRWEuO5PSw",
        "ChIJA9mv03AbyYcRmQE0_RZlBc8",
        "ChIJL7osmQcDyYcRlXC12J619Kk",
        "ChIJWZJnTo732I4RXOOOGdgErrE",
        "ChIJk05_KLw9yYcRdILLlzlgZbc",
        "ChIJ4R35hVgZyYcRtWaZ2pEeZbg",
        "ChIJ6cmQcpObkwMR6y1gU2JuIyg",
        "ChIJW_eAh-AFyYcRvehA8EHTKpg",
        "ChIJxZ3nMNaNZUQRDRy_oZRijYE",
        "ChIJtZuTzekSyYcRCimNYowXt2o",
        "ChIJO4kwAFk53QkRkArhcqhZ0BA",
        "ChIJ31Fx-bkRyYcR_SK-o2oKl_A",
        "ChIJQdlsGVULyYcRNsqDrEWwlPI",
        "ChIJP4wImcYQyYcRZIH_qsh9pMg",
        "ChIJl7MIgiK2o04RV5obMBs2D8M",
        "ChIJh9Q-kijRGIUR8NNqo8Av1XU",
        "ChIJBxRN8viXyYcRUdw5VTbb4K0",
        "ChIJJ6BiEb7YBaMRZtmr-oJNWTs",
        "ChIJNeoNdZtryYcR-sb2NhJxu8c",
        "ChIJs9FCFR2duIkRoPoopajKpK0",
        "ChIJCXQyG7TjSogRYDzm8xStzAk",
        "ChIJpUDNz0VpyYcRdzXNalU2EFU",
        "ChIJ4zyW2VfuyIcRjDYDqdrTjBc",
        "ChIJCcP8tivvyIcRSDcMFLmfeJY",
        "ChIJr9FTWuMXYa8RODsMgyP4osY",
        "ChIJLfeziAw_yYcRlQ4dvNIm7Ec",
        "ChIJqf9JhfEXyYcRmQU6rGSjsfU",
        "ChIJUTOiU54VyYcRofbbwWiSh48",
        "ChIJk2fjmU6jyYcRlh0r36Fmxxo",
        "ChIJmeR1LJJryYcRGDLs_OaQy-g",
        "ChIJ01Gxt3FTzIcRPuYcp_ziPN0",
        "ChIJC6GpNPlSzIcRHSxz7el2OaA",
        "ChIJFyYoaqZTzIcRrmTdw7b6bPE",
        "ChIJ5wxGj1hTzIcRpm1PEtF2yy8",
        "ChIJo5L2URdTzIcRKm_2bjafSDg",
        "ChIJybKL2W5TzIcRyg3V3rabb9A",
        "ChIJPTfpgPdVzIcR39bBexfMt3E",
        "ChIJsZUSNWhkJkERoPrAbKC-sY4",
        "ChIJz_IWez6Ky4cRaBj9e9Busog",
        "ChIJPSyqQGYGbKoRG7_jbx26N3o",
        "ChIJob7fFS8QhUMR0S_h2hHsyKc",
        "ChIJbTGjjU0VIGkRRzx1BeJ6yZU",
        "ChIJLbdFML2pzYcR6jGXgnuRqOQ",
        "ChIJFWQoopypzYcRJcRe5w8wXYc",
        "ChIJZbHX9OJLzIcRmXJ-uOhlS60",
        "ChIJ4yv2GzexzYcRWB-m5kBBk5I",
        "ChIJ93kFXXADM4YRngHmBesCES4",
        "ChIJR9MjaDVFzIcR5avoJVl4HP4",
        "ChIJ94uSK75BzIcRMVgllOFqOUg",
        "ChIJuy2OD22W-isR1IVLNzBWGUU",
        "ChIJjTKrGVaWBSERdaDHR-YtR6o",
        "ChIJF66ylsWrzYcRqbNOqAuAauo",
        "ChIJvaDDG217FQER447PudrS5jc",
        "ChIJUwPOraMfByYR-z70NTRgQTY",
        "ChIJQ8x1nECXYgsRaXW9Sizrbag",
        "ChIJRcIz0B6LsSkRycEthRci2p4",
        "ChIJCQjhiGX2yocRtCnS5asLCE0",
        "ChIJFaXmFROFy4cRbamqr_safpk",
        "ChIJo9HuUpVN0ocRZUzLlafA9iY",
        "ChIJbXQs7kp4eCERMEYEb0GLjb0",
        "ChIJR9OIQfhLh4gRxV9uS5PlvgU",
        "ChIJl5JNf5hOh4gRQqqJd_EhWx4",
        "ChIJW9aIInlFh4gRMa5cFLdWbYY",
        "ChIJ3efxnNXFfYgR9cMZpAZMuXQ",
        "ChIJrehgvxROzYcR-YCz3kwduQM"
    ]

    # Configure the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    all_results = []
    simplified_reviews = []
    batch_size = 10  # Process in batches of 10

    print(f"Found {len(place_ids)} place IDs to process")

    # Process in batches
    for i in range(0, len(place_ids), batch_size):
        batch = place_ids[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1} of {(len(place_ids)-1)//batch_size + 1} ({len(batch)} place IDs)")

        payload = {
            "placeIds": batch,
            "language": "en",
            "maxReviews": 0,  # No limit - get all available reviews
            "includeNonTextReviews": False
        }

        try:
            start_time = time.time()
            print(f"Sending request to Apify...")
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()

            # Add results to our collection
            batch_results = response.json()
            all_results.extend(batch_results)

            elapsed_time = time.time() - start_time
            print(f"Successfully scraped {len(batch_results)} reviews in {elapsed_time:.1f} seconds")

            # Immediately process this batch to simplified format
            for review in batch_results:
                # Format the date nicely
                try:
                    pub_date = datetime.fromisoformat(review.get('publishedAtDate', '').replace('Z', '+00:00'))
                    formatted_date = pub_date.strftime('%Y-%m-%d')
                except (ValueError, TypeError):
                    formatted_date = review.get('publishAt', 'Unknown date')

                business_name = review.get('title', 'Unknown Business')
                place_id = review.get('placeId', 'Unknown Place ID')

                simplified_review = {
                    "business_name": business_name,
                    "place_id": place_id,
                    "reviewer_name": review.get('name', 'Anonymous'),
                    "text": review.get('text', ''),
                    "date": formatted_date,
                    "stars": review.get('stars', 0)
                }
                simplified_reviews.append(simplified_review)

            # Save partial results after each batch
            with open(f'reviews_batch_{i//batch_size + 1}.json', 'w') as f:
                json.dump(simplified_reviews[-len(batch_results):], f, indent=2)

            print(f"Saved batch results to reviews_batch_{i//batch_size + 1}.json")

            # Add a delay between batches to avoid rate limiting
            if i + batch_size < len(place_ids):
                delay = 10  # 10 seconds between batches
                print(f"Waiting {delay} seconds before next batch...")
                time.sleep(delay))

        except requests.exceptions.RequestException as e:
            print(f"Error processing batch: {e}")
            print("Saving error information...")
            with open(f'error_batch_{i//batch_size + 1}.txt', 'w') as f:
                f.write(f"Error occurred at: {datetime.now()}\n")
                f.write(f"Batch: {batch}\n")
                f.write(f"Error: {str(e)}\n")
            print(f"Continuing with next batch in 30 seconds...")
            time.sleep(30)
            continue

    # After all batches, combine and save final results
    try:
        print("\nProcessing complete! Combining all results...")

        # Save all results to a single file
        with open('all_google_reviews.json', 'w') as f:
            json.dump(all_results, f, indent=2)

        # Save simplified version
        with open('simplified_reviews.json', 'w') as f:
            json.dump(simplified_reviews, f, indent=2)

        # Create an organized version by business
        reviews_by_business = {}
        for review in simplified_reviews:
            business_name = review['business_name']
            place_id = review['place_id']
            key = f"{business_name} ({place_id})"

            if key not in reviews_by_business:
                reviews_by_business[key] = []

            # Remove business info from individual reviews to avoid duplication
            review_copy = review.copy()
            del review_copy['business_name']
            del review_copy['place_id']
            reviews_by_business[key].append(review_copy)

        with open('reviews_by_business.json', 'w') as f:
            json.dump(reviews_by_business, f, indent=2)

        print(f"\nScraping and processing complete!")
        print(f"Total reviews collected: {len(all_results)}")
        print(f"Total businesses: {len(reviews_by_business)}")
        print(f"Results saved to three files:")
        print(f"1. all_google_reviews.json - Full data")
        print(f"2. simplified_reviews.json - Simplified format")
        print(f"3. reviews_by_business.json - Organized by business")

    except Exception as e:
        print(f"Error in final processing: {e}")
        print("Individual batch results are still available in the batch files.")

    return all_results

if __name__ == "__main__":
    scrape_all_reviews()