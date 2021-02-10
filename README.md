# dpc-covid-data

![get_data_from_iss](https://github.com/giovanniardenghi/dpc-covid-data/workflows/get_data_from_dpc/badge.svg)
[![GitHub commit](https://img.shields.io/github/last-commit/giovanniardenghi/dpc-covid-data)](https://github.com/giovanniardenghi/dpc-covid-data/commits/main)

Serie storica dei dati della sorveglianza integrata COVID-19 in Italia. I dati sono disponibili nel folder [`data`](data) di questo repository.

## Stato degli aggiornamenti

I dati vengono aggiornati ogni 15 minuti. Il [badge](#dpc-covid-data) a inizio pagina è di colore verde se gli aggiornamenti stanno funzionando senza errori. Per ulteriori dettagli, verificare i log del [workflow di aggiornamento](https://github.com/giovanniardenghi/dpc-covid-data/actions?query=workflow%3Aget_data_from_dpc).

Il dato giornaliero viene rilasciato quotidianamente dal Dipartimento di Protezione Civile in [questa repository](https://github.com/pcm-dpc/COVID-19/tree/master/).

Questa repository funge da backup per la dashboard [epiMOX](https://www.epimox.polimi.it) sviluppata dal laboratorio MOX del dipartimento di matematica del Politecnico di Milano.
