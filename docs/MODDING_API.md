# Ad Astra — public triggers for other mods

Ad Astra: Origins starts an empire as a pre-FTL civilization confined to its
homeworld, and opens content age by age. Content added by other mods does not
know about those ages, so it can appear too early. These scripted triggers let
another mod lock its own content on Ad Astra's progression, without reading
Ad Astra's internal flags and without depending on Ad Astra.

They are defined in `common/scripted_triggers/zzzz_adastra_api.txt` and are
kept stable across versions.

| Trigger | Scope | True when |
|---|---|---|
| `adastra_api_loaded = yes` | any | Ad Astra is active in this game |
| `adastra_api_is_confined = yes` | country | the empire is an Ad Astra empire still confined to its homeworld |
| `adastra_api_has_reached_age = { AGE = <age> }` | country | the empire has reached that age (ages accumulate) |
| `adastra_api_has_emerged = yes` | country | the empire has completed its ascent (Hyperdrive) |
| `adastra_api_gigastructures_loaded = yes` | any | Gigastructural Engineering & More is active |

Ages, in order: `stone`, `bronze`, `iron`, `medieval`, `renaissance`,
`steam`, `industrial`, `machine`, `atomic`, `space`.

## Using them without depending on Ad Astra

Declare the triggers you use in your own mod with a neutral value, in a file
whose name sorts **before** `zzzz_adastra_api.txt` (for example
`00_mymod_adastra_compat.txt`):

```
adastra_api_is_confined = { always = no }
adastra_api_has_reached_age = { always = no }
```

When Ad Astra is not active, your neutral version is used. When it is, Ad
Astra's file loads after yours and replaces it. This is the same mechanism as
Gigastructural Engineering's compatibility triggers.

## Examples

Hide a tradition category until an Ad Astra empire has emerged:

```
potential = {
	NOT = { adastra_api_is_confined = yes }
}
```

Open a building from the Steam Age for Ad Astra empires, and normally for
everyone else:

```
potential = {
	OR = {
		NOT = { adastra_api_is_confined = yes }
		adastra_api_has_reached_age = { AGE = steam }
	}
}
```

## Contact

Questions and compatibility reports: the Ad Astra Discord
(https://discord.gg/nKP4TfNzNX) or GitHub issues
(https://github.com/ampynjord/ad-astra-stellaris/issues).
