# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 11370  GET              /                                                dashboard
 12888  GET              /api/abo/status                                  api_abo_status
 12869  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11987  GET              /api/automation/status                           api_automation_status
 12009  POST             /api/automation/toggle                           api_automation_toggle
 21490  GET              /api/channel/categories                          api_channel_categories
 21496  POST             /api/channel/set                                 api_channel_set
 21347  GET              /api/channels/status                             api_channels_status
 21049  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 21032  GET              /api/clips                                       api_clips
 21078  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20978  GET              /api/debug/threads                               api_debug_threads
 12874  GET              /api/events                                      api_events
 12365  GET              /api/events/stream                               api_events_stream
 12224  GET              /api/health                                      api_health
 21009  POST             /api/highlights/config                           api_highlights_config
 11300  POST             /api/login                                       dashboard_login_submit
 13106  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12294  GET              /api/notify/status                               api_notify_status
 12305  POST             /api/notify/test                                 api_notify_test
 12942  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12919  GET              /api/proxy/trend                                 api_proxy_trend
 21096  GET              /api/tts/<fn>                                    api_tts_file
 21873  GET              /api/upload_window                               api_upload_window
 12467  GET              /archive/<int:eid>/download                      archive_download
 12493  GET              /download/<int:recording_id>                     download
 12426  GET              /health                                          health
 20850  GET              /healthz                                         healthz
 11291  GET              /login                                           dashboard_login_page
 11325  GET              /logout                                          dashboard_logout
 11332  GET              /manifest.webmanifest                            pwa_manifest
 21854  GET              /overlay                                         overlay_page
 11356  GET              /pwa-icon-<variant>.png                          pwa_icon
 11342  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (357)

```
   195  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   422  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
  1074  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   776  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   941  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   921  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   959  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   879  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   387  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   398  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   408  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   431  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   438  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   449  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   582  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   680  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1315  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1347  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   372  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
  1027  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
  1003  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1180  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1228  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1282  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1138  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   978  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   548  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   827  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   694  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   677  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   669  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   482  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   498  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   871  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   400  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   431  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   836  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   856  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   728  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    86  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   238  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   263  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   268  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   417  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   408  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   343  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   230  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   196  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   179  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   399  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   532  GET              /api/beobachtung/dienste                         api_beobachtung_dienste   [nc/routes/beobachtung.py]
   525  GET              /api/beobachtung/lage                            api_beobachtung_lage   [nc/routes/beobachtung.py]
   547  POST             /api/beobachtung/steuern                         api_beobachtung_steuern   [nc/routes/beobachtung.py]
   376  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   174  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    39  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    51  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   443  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   556  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   528  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   253  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   188  POST             /api/cookies/bereinigen                          api_cookies_bereinigen   [nc/routes/settings.py]
   133  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    74  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    81  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   496  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   274  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   301  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   399  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   338  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   356  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   261  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    86  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   132  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   146  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   161  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
    56  GET              /api/einstellungen                               api_einstellungen   [nc/routes/einstellungen.py]
    68  POST             /api/einstellungen                               api_einstellungen_setzen   [nc/routes/einstellungen.py]
   102  POST             /api/einstellungen/uebernehmen                   api_einstellungen_uebernehmen   [nc/routes/einstellungen.py]
    86  POST             /api/einstellungen/zuruecksetzen                 api_einstellungen_zuruecksetzen   [nc/routes/einstellungen.py]
   193  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   178  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    89  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   111  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   132  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   149  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    79  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   208  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    43  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   229  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   249  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   276  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   394  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   297  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   414  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   409  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   485  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   307  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   161  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    44  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   151  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   126  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   182  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    77  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
   100  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   216  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   847  GET              /api/ki/wahl                                     api_ki_wahl   [nc/routes/ai.py]
   856  POST             /api/ki/wahl                                     api_ki_wahl_setzen   [nc/routes/ai.py]
   225  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   247  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   174  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   152  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   131  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   181  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
    66  GET              /api/lagebild                                    api_lagebild   [nc/routes/lagebild.py]
   173  GET              /api/leitstand                                   api_leitstand   [nc/routes/leitstand.py]
   428  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    79  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   111  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   121  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    53  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    71  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   146  GET              /api/mcp/export                                  api_mcp_export   [nc/routes/mcp.py]
    85  GET              /api/mcp/server                                  api_mcp_server_liste   [nc/routes/mcp.py]
   111  POST             /api/mcp/server                                  api_mcp_server_anlegen   [nc/routes/mcp.py]
   116  POST             /api/mcp/server/<sid>                            api_mcp_server_aendern   [nc/routes/mcp.py]
   121  DELETE           /api/mcp/server/<sid>                            api_mcp_server_loeschen   [nc/routes/mcp.py]
   132  POST             /api/mcp/server/<sid>/test                       api_mcp_server_test   [nc/routes/mcp.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   101  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    67  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    78  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   148  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   143  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   134  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    54  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    93  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   257  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   324  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   352  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   203  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   270  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   505  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   168  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   151  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   391  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   238  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   326  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   293  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
   171  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   268  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   590  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   565  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   992  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1133  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1161  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1181  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   979  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1041  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1028  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
  1009  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   647  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   642  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   690  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   573  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   907  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   664  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   627  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   600  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   881  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   744  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   840  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   739  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   672  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   463  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   924  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   551  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   802  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   957  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   942  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   507  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   734  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   720  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   703  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   760  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1324  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1478  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1288  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   860  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   749  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   509  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   487  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   553  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   570  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   622  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   459  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   274  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   167  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   644  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   422  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   136  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   583  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   609  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   200  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   225  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   397  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   148  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   160  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   614  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   604  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   644  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   366  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   456  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   578  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   397  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   427  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   219  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    74  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   118  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   141  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   105  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   375  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   389  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   189  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   239  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   460  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   489  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   409  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   422  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   518  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   395  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   270  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   315  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   339  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   326  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   166  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   284  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   135  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   376  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   431  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   265  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   453  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   419  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   478  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   458  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   441  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   434  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   251  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   317  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
    73  GET              /fonts/<name>                                    schrift   [nc/routes/schriften.py]
    66  GET              /fonts/schriften.css                             schriften_css   [nc/routes/schriften.py]
   469  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
   133  GET              /overlay/chat                                    overlay_chatbild   [nc/routes/overlay.py]
   148  GET              /overlay/chat.json                               overlay_chatbild_daten   [nc/routes/overlay.py]
```

## Discord-Slash-Commands in discordbot.py (67)

```
  2728  /about                  Ueber diesen Bot
  1269  /ai                     
  2728  /aireset                KI-Kontext zuruecksetzen
  1714  /ask                    
  1370  /assign_role            
  1428  /ban                    
  2684  /botstats               
  2728  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2728  /bulkadd                Mehrere User auf einmal tracken · a b c
  2728  /cleanup                Alte Aufnahmen aufraeumen
  1987  /clearwarns             
  2648  /clip                   
  2633  /clipoftheweek          
  1850  /clips                  
  2728  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1325  /create_category        
  1296  /create_channel         
  1360  /create_group           
  1335  /create_role            
  1311  /create_voice           
  1591  /daily                  
  2728  /diag                   Vollstaendige Diagnose
  2728  /einnahmen              Einnahmen und Spenden
  1743  /event                  
  1785  /events                 
  1890  /follow                 
  1879  /help                   
  1416  /kick                   
  1563  /leaderboard            
  2728  /live                   Live-Status sofort pruefen · @user
  1837  /livenow                
  2728  /logs                   Letzte Fehler aus dem Log
  2728  /pause                  Tracking pausieren · @user
  1865  /post_test              
  1675  /profile                
  1454  /purge                  
  2728  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2728  /quota                  Speicher-Quota
  1550  /rank                   
  1825  /recstatus              
  1382  /remove_role            
  2728  /report                 Azrael-Sentinel-Wochenreport
  1282  /restream_status        
  2728  /resume                 Tracking fortsetzen · @user
  1394  /set_channel_perms      
  1514  /setup_community        
  1531  /setup_targets          
  1811  /spenden                
  1924  /stats                  
  1241  /status                 
  2728  /stoprec                Laufende Aufnahme sauber beenden · @user
  2025  /streaminfo             
  2728  /summary                Tageszusammenfassung
  2728  /sysres                 System-Ressourcen
  2728  /teststream             Recorder-Selbsttest · @user
  2728  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1440  /timeout                
  1997  /topstreamers           
  2728  /topusers               Top-Streamer nach Aufnahmen
  1150  /track                  
  2728  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
  1254  /tracklist              
  1906  /unfollow               
  2728  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
  1203  /untrack                
  1945  /warn                   
  1973  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2832  on_member_join
  2789  on_message
  2749  on_raw_reaction_add
  2869  on_ready
```

## Top-Level-Symbole in telegramversand.py (10 Funktionen)

```
   456-460    _fehler_meldung
   557-585    _nachteilen
   588-618    _neu_kodiert
   463-526    _teile_bereiten
   416-433    _teile_freigeben
   401-413    _teile_holen
   529-554    _teilen_oder_reparieren
    59-74     konfiguriere
    77-384    split_and_send_video
   436-453    teil_pause_s
```

## Top-Level-Symbole in discordbot.py (70 Funktionen)

```
  2132-2183   _award_xp
  1468-1484   _bereiche_bericht
   557-568    _clip_kopieren
  2348-2377   _clip_week_leader
  2401-2412   _clipoftheweek_loop
   668-721    _clips_einsortieren
  2988-3052   _community_events_loop
   359-368    _dc_abbruch_melden
  2102-2108   _dc_bereit
  2059-2081   _dc_client
   342-356    _dc_fehlerart
  2084-2093   _dc_offen
  2111-2123   _dc_warten
  3092-3127   _disc_automod_check
   475-480    _disc_sprache_setzen
  2186-2234   _discord_ai_automod
   893-935    _discord_automod
  2237-2257   _discord_azrael_reply
  2552-2945   _discord_run_once
   249-326    _discord_start
   371-425    _ensure_discord_invite
  2951-2985   _ensure_error_channel
   504-517    _ensure_rank_roles
  1113-1127   _ensure_team_roles
  3055-3085   _error_channel_loop
   952-966    _follow_erlaubt
   611-615    _getrackte_nutzer
   945-949    _guard
   826-890    _handle_voice_ai
   483-501    _is_admin
   583-608    _link_video
  2302-2310   _liveboard_loop
   969-971    _name_ungueltig
  1007-1041   _on_level_up
   749-750    _par_chat_id
  2380-2398   _post_clip_of_week
  2313-2331   _post_weekly_digest
   520-546    _provision_base_channels
   984-1004   _rang_pruefen
   974-981    _rang_satz
  1817-1913   _reg_betrieb
  1487-1580   _reg_community_setup
  1583-1664   _reg_daily_profil
  1707-1804   _reg_frage_events
  1228-1284   _reg_info
  1408-1465   _reg_moderation
  1667-1704   _reg_profil
  1351-1405   _reg_rollen
  1287-1348   _reg_server
  1807-1814   _reg_spenden
  1916-2008   _reg_streamer
  2011-2056   _reg_system
  1141-1225   _reg_tracking
  1076-1110   _run_tg_handler
   812-823    _shim_chat_id
  2510-2539   _stern_an_telegram
  2542-2549   _stern_anspruch_zurueck
  2415-2507   _stern_highlight
   166-228    _uebernehmen
   571-580    _umzugsmarken
  2266-2299   _update_liveboard
   798-809    _voice_dauer
   769-776    _voice_max_s
   779-795    _voice_zulassen
  2334-2345   _weekly_digest_loop
   549-554    _ziel_guild
   618-665    _ziele_abgleichen
   730-746    _ziele_sync_loop
   724-727    _ziele_takt_min
   231-234    starte
```

## Top-Level-Symbole in bot.py (594 Funktionen, 4 Klassen)

```
 26768-26790  _abbruch_datenbank_unlesbar
  2882-2883   _abo_key
  2903-2921   _abo_probe_dump
 26890-26906  _abschied_wachen
 26909-26927  _abschluss
 17059-17066  _ad_allowlist
 18225-18231  _agent_for
 18234-18250  _ai_telemetry
 18766-18784  _alert
 22294-22344  _alert_monitor_loop
 19471-19528  _alte_beilagen_einsammeln
 22731-22793  _announce_loop
  3833-3843   _anthropic_key
  3846-3848   _anthropic_model
 10823-10826  _arg_int
  2874-2879   _as_dict
 26454-26463  _async_exc_handler
 18955-18977  _audio_tap_cmd
 19998-20057  _audio_tap_melden
 18991-19015  _audio_tap_sammler
 23054-23089  _aufnahme_an_server
 10171-10208  _aufnahme_beim_stopp_sichern
 19413-19434  _aufnahme_chat_ausklang
 19397-19410  _aufnahme_chat_beginnen
 19556-19577  _aufnahme_chat_dienst
 19756-19811  _aufnahme_chat_einarbeiten
 19392-19394  _aufnahme_chat_modus
 19580-19629  _aufnahme_chat_nachtrag
 19437-19468  _aufnahme_chat_vormerken
 19547-19553  _aufnahme_chat_wecken
 25570-25572  _aufnahme_deckel
 19632-19653  _aufnahme_fertigmachen
 22977-23037  _aufnahme_nach_discord
 10211-10229  _aufnahme_platz_frei
 10096-10141  _aufnahme_verteilen
 26854-26874  _aufnahmen_abschliessen
 26793-26851  _aufraeumen
 11112-11181  _auth_cookie
 11066-11108  _auth_guard
  2129-2134   _auto_on
 20713-20739  _auto_restream_loop
 14373-14415  _avatar_frames_laden
 17109-17122  _azrael_brain_kontext
 24002-24017  _azrael_broadcast_reply
 23902-23924  _azrael_chat_reply
 23874-23899  _azrael_chat_should_reply
 23930-23932  _azrael_gate_cfg
  4377-4392   _azrael_ki
 18253-18267  _azrael_live_state
  4395-4418   _azrael_lokal
 21740-21754  _azrael_overlay_state
 18309-18317  _azrael_persona_kern
 18648-18702  _azrael_proactive_loop
 18073-18129  _azrael_reaction_to_chats
 23935-23942  _azrael_reply_all_chats
  4421-4436   _azrael_schweigt_melden
 23861-23871  _azrael_self_names
 23970-23999  _azrael_send_to
 14334-14370  _azrael_spricht
 14692-14705  _azrael_stimme_stumm
 18273-18306  _azrael_system
 22428-22431  _backup_active
 22509-22522  _backup_loop
  5635-5658   _betreiber_pruefen
 25659-25663  _betrieb
 26527-26536  _brain_crowdsec_snap
 26695-26698  _brain_db_health
 24861-24901  _brain_fragen
 22215-22224  _brain_growth_loop
 11499-11526  _brain_growth_snapshot
  2793-2827   _brain_hint_delay
 26599-26634  _brain_moderation_snap
  6955-6983   _brain_notify
 26701-26723  _brain_recording_snap
 26539-26596  _brain_restream_health
 26726-26739  _brain_tiktok_status_snap
 12340-12361  _browser_push
 14739-14743  _build_restream_cmd
  5661-5688   _can_stop_tracking
  2240-2262   _capture_set_cookies
 12972-12975  _cfg_get
 12978-12980  _cfg_set
 21451-21486  _channel_set_all
 13415-13418  _chat_connected
 13421-13437  _chat_disconnected
 19541-19544  _chat_einarbeiten_async
  9587-9617   _chat_is_forum
 19361-19386  _chat_listener_abbauen
  9759-9794   _chat_migriert
  9797-9798   _chat_migriert_async
 13451-13453  _chat_sanitize
 13400-13412  _chat_stat
  4251-4263   _check_ai_models_sync
 11694-11737  _classify_pool_anonymity
   920-942    _claude_chat_sync_metered
 10868-10874  _client_ip
 23503-23517  _clip_chat_ass
 22877-22920  _clip_prune
 22923-22933  _clip_recfile_for
 23417-23491  _clip_schneiden
 23520-23526  _clip_should_velocity
 23092-23178  _clip_to_discord
 19727-19732  _clips_abwarten
  4033-4042   _close_ai_session
 24048-24063  _cohost_broadcast
 24033-24034  _cohost_cfg
 24089-24101  _cohost_fire_highlight
 24037-24045  _cohost_gate
 24066-24086  _cohost_highlight
  7285-7346   _cookie_alarm_loop
  2330-2331   _cookie_autofetch_info
  2314-2318   _cookie_autorefresh_info
 26124-26146  _cookie_bezug_loop
 26149-26174  _cookie_bezug_runde
  2217-2221   _cookie_header
 10877-10882  _cookie_sicher
  2343-2357   _cookies_selbst_holen
  4526-4528   _create_index_safe
  7171-7198   _daily_summary_loop
  3359-3384   _darf_ytdlp_nachschlagen
 12508-12529  _dashboard_adresse
 10897-10901  _dashboard_hostnamen
  1540-1570   _dashboard_trackings_umziehen
 23494-23500  _datei_weg
 22268-22291  _db_maintenance_loop
  7121-7168   _db_vacuum_loop
 12532-12541  _deck_intern_url
 17082-17106  _detect_foreign_ad
  1810-1821   _diag_path_owner
 18553-18598  _director_finalize
 19988-19995  _director_for
 18502-18550  _director_mark
 23330-23333  _disc_state_get
 23336-23343  _disc_state_set
 23040-23051  _discord_aufnahme_gilden
 22196-22205  _discord_bot_starten
 22159-22170  _discord_einladung_merken
 22208-22212  _discord_invite
 22173-22193  _discord_kontext
 23291-23327  _discord_live_thread
 18705-18717  _discord_notify
 22131-22156  _discord_ops_alert
 23189-23287  _discord_post_user
 22796-22802  _discord_stop
  7201-7282   _disk_alarm_loop
 25995-26046  _disk_autoclean
 26310-26323  _disk_guard_loop
 14313-14320  _drossel_hoeher
 14309-14310  _drossel_stufe
 14323-14331  _drossel_zuruecksetzen
 12710-12712  _dump_all_threads
 25666-25680  _einstellungen_startzeile
  2382-2443   _ensure_cookie_file_netscape
  9688-9691   _ensure_notify_topic
 11844-11881  _ensure_proxy_ready
  9627-9650   _ensure_topic
   763-765    _env_int
   768-770    _env_int_range
 18750-18763  _event_webhook
 13198-13211  _evolution_loop
  6361-6395   _extract_file_payload
  1522-1537   _fanout_ziele
 26930-26995  _fatal_vom_botteil
 25575-25590  _fd_grenze_anheben
  5203-5213   _fehler_text
 11593-11611  _fetch_proxy_list
 19330-19358  _fetch_tiktok_room_id
   848-851    _ff_cmd
 19740-19753  _ffprobe_masse
 14237-14253  _fifo_schreiber_wecken
 14025-14030  _find_chromium
  3754-3756   _find_external_recorder
  2506-2508   _find_stream_urls
 13021-13046  _fire_webhooks
  8234-8244   _fork_safe
   953-966    _freeai_chat_sync_metered
  4021-4030   _get_ai_session
  8062-8102   _get_live_info
  3203-3210   _get_resolve_semaphore
  8759-9194   _handle_single_tracking
 25779-25781  _hb
 25784-25801  _hb_while
 20963-20974  _healthz_fuer_aufrufer
 25825-25853  _heap_zurueckgeben
 11185-11202  _herkunft_guard
 13465-13467  _highlight_cfg
 13470-13499  _highlight_observe
 12544-12554  _htmlov_basis_url
 14097-14105  _htmlov_bild_schreiben
 14066-14094  _htmlov_dauerbrowser
 14045-14063  _htmlov_screenshot_cmd
 14033-14042  _htmlov_url
 19017-19027  _httpx_proxy
 13054-13066  _in_quiet_hours
 26754-26765  _init_db_oder_abbruch
 27609-27640  _install_fast_eventloop
 10718-10772  _install_fast_json
 12715-12731  _install_faulthandler
 20759-20768  _intel_ensure_schema
 20811-20846  _intel_index_loop
 20780-20795  _intel_index_one
 20771-20777  _intel_semantic
  5613-5633   _is_authorized
  8585-8606   _is_dead
  2029-2036   _is_process_running
  6985-6992   _is_quiet_hours
  1411-1420   _is_upload_window
  5035-5050   _iso
 10885-10894  _ist_lokal
 10807-10820  _json_error_handler
  4095-4114   _ki_nach_deckwahl
  4172-4181   _ki_rueckfall_melden
  8460-8467   _kick_cluster_gefunden
  8395-8457   _kick_cluster_weiter
  7034-7076   _kick_follower_count
  7018-7021   _kick_slug
  8365-8392   _kick_ws_pause
 26742-26751  _kickmod_boot
 26090-26093  _lagebild_discord_aufnahme
 26103-26107  _lagebild_kick_chat
 26096-26100  _lagebild_overlay
 26110-26112  _lagebild_spendenziel
 26077-26087  _lagebild_upload
 13083-13085  _latest_popularity
  1966-1975   _laufstand
 26265-26307  _laufstand_loop
 25703-25741  _leistung_erheben
  7951-7978   _link_video_senden
  8746-8757   _live_check_frist_melden
  2937-2950   _live_ohne_stream
 20396-20445  _live_react_loop
 20060-20382  _live_react_worker
  3602-3716   _live_status_aufloesen
 18132-18143  _live_transcript_push
 20384-20394  _live_users
 18601-18645  _living_title_loop
 22434-22506  _local_backup_scan
  4969-4998   _lock_update
 10789-10803  _log_5xx
 25744-25776  _log_schleuse_pruefen
   838-845    _log_sicher
 14751-14763  _looks_like_codec_err
 14746-14748  _looks_like_source_expired
  8283-8313   _loop_fehler
 12734-12743  _loop_heartbeat
 25481-25514  _loop_lag_monitor
 25528-25548  _loop_stockung_melden
 25551-25561  _loop_takt_starten
 12746-12819  _loop_watchdog_thread
 18009-18026  _loyalty_add
 18000-18006  _loyalty_get
 18029-18037  _loyalty_top
  5314-5333   _manual_status
  8608-8609   _mark_dead
 12064-12080  _marketing_loop
 23949-23967  _maybe_handle_command
 26409-26433  _maybe_hype_clip
 22846-22874  _meme_klassifizieren
 19656-19724  _meme_zusammenschnitt
  4513-4518   _migrate_columns
 24231-24242  _mod_is_exempt
 24245-24250  _mod_warn_first
 24253-24256  _mod_warn_text
 13240-13259  _modlog
 13223-13237  _modlog_schreiben
  1104-1106   _multistream_targets
  3387-3423   _nachschlag_ytdlp
  8247-8248   _nc_create_subprocess_exec
  8251-8252   _nc_create_subprocess_shell
 12178-12195  _news_loop
 13282-13284  _normalize_ingest
  2724-2741   _note_check_duration
  9682-9685   _notify_topic_name
  4117-4122   _nur_free
  4125-4129   _nur_free_sync
  4132-4169   _nur_lokal_sync
  2928-2934   _offline_ergebnis
  3426-3449   _ohne_url_melden
 18158-18166  _oracle_memories
 18453-18487  _oracle_memorize
 18169-18182  _oracle_persona
 18151-18155  _oracle_recent_text
 13688-13689  _ov_atomic_write
 13679-13681  _ov_bar
 16987-16999  _ov_clip_text
 13684-13685  _ov_oneline
 13778-13839  _overlay_kanalweit
 21789-21847  _overlay_push
 13979-14022  _overlay_render_size
 13842-13869  _overlay_sendebild_schreiben
 13351-13355  _overlay_session_reset
 21756-21758  _overlay_src_ok
 13698-13710  _overlay_takt
 17069-17079  _own_invites
 13974-13976  _parse_size
  7596-7629   _pause_resume_cmd
  2268-2312   _persist_refreshed_cookies
  2171-2203   _pick_checked_pull_proxy
 10951-10966  _pin_auth_value
 11055-11056  _pin_clear_fail
 11019-11022  _pin_global_gesperrt
 10972-10983  _pin_hmac_schluessel
 11025-11032  _pin_locked
 11035-11052  _pin_note_fail
 10986-11007  _pin_ok
 21584-21609  _piper_pick_model
 21669-21734  _piper_say
 12983-13018  _post_json_threaded
 13953-13971  _probe_video_size
  2057-2074   _proc_is_recorder
 11813-11841  _proxy_pool_refresh_loop
  2137-2168   _proxy_report_recording
  9333-9417   _pruef_runde
  9292-9330   _pruefstand_melden
 25610-25621  _pruefung_verworfen
 12700-12702  _prune_stall_dumps
  2334-2340   _pull_proxy_still
 18721-18747  _push_notify
 11249-11251  _pwa_dir
 11662-11679  _quick_validate_proxy
 13049-13051  _quiet_hours_config
 11214-11247  _rate_guard
  2953-2981   _raumsperre_fragen
 17970-17976  _react_warn
  8149-8188   _reap_proc
 10904-10920  _rebinding_melden
 10026-10093  _rec_auto_abschalten
  9973-10023  _rec_frueh_getrennt
  9838-9918   _rec_kategorie_melden
  9921-9970   _rec_totstreak_fortschreiben
  2764-2786   _record_check_outcome
   833-835    _redact_stream_urls
 11740-11810  _refresh_proxy_pool
  2541-2632   _resolve_via_html
  2984-3180   _resolve_via_webcast_api_v2
  3248-3335   _resolve_via_ytdlp
 23560-23689  _resolve_youtube_ingest
  2517-2538   _resolver_stumm
 13334-13345  _restream_active_sources
 14418-14556  _restream_avatar_feeder_start
 14559-14569  _restream_avatar_feeder_stop
 19814-19952  _restream_chat_guardian
 13502-13587  _restream_chat_push
 13664-13674  _restream_chat_push_async
 14256-14273  _restream_chatbild_start
 26637-26692  _restream_durchreicher
 14108-14234  _restream_html_overlay_start
 14276-14296  _restream_html_overlay_stop
 20697-20710  _restream_liste_abgleichen
 13293-13316  _restream_overlay_files
 20448-20480  _restream_platform_state
 20656-20691  _restream_resume_after_restart
 13618-13635  _restream_soll_schreiben
 13638-13661  _restream_status_schreiben
 14617-14689  _restream_tts_enqueue_wav
 13915-13947  _restream_tts_feeder
 13912-13913  _restream_tts_fifo_path
 14572-14599  _restream_tts_start
 14601-14615  _restream_tts_stop
 20486-20653  _restream_verify_loop
 22399-22411  _retention_loop
 22393-22396  _retention_scan
  2885-2887   _room_is_abo
  6398-6553   _run_ai_call
 12842-12855  _run_async_from_flask
 27598-27606  _run_selfcheck_and_exit
 22414-22425  _s3_client
  8635-8705   _safe_send
  5277-5293   _sample_net_throughput
 27578-27595  _sc_bericht
 27519-27575  _sc_dienste
 27426-27516  _sc_ki_und_stimme
 27377-27423  _sc_umgebung
  2830-2860   _schedule_next_check
 22347-22390  _scheduler_loop
  4521-4523   _schema_pk
 12858-12863  _scraper_session
 24259-24298  _screen_full
 12240-12277  _sec_headers
  2501-2503   _select_stream_from_data_section
 27287-27374  _selfcheck
  9694-9728   _send_live_notice
  1434-1438   _should_defer_upload
 22936-22974  _shrink_for_discord
 11254-11287  _sicheres_ziel
 22227-22265  _sicherheits_erinnerung_loop
 26330-26347  _sign_health_check
 26350-26369  _sign_health_loop
  5053-5083   _sitzung_bestimmen
 20946-20956  _sparen_lage
  8264-8275   _spawn
 28031-28061  _spawn_from_flask
 25624-25630  _speicher_maps
 25633-25648  _speicher_pflegen
 19029-19327  _start_chat_listener
 25593-25607  _start_gesperrt
 12822-12839  _start_loop_watchdog
 12126-12175  _stats_loop
 12105-12108  _stats_output_path
 12111-12123  _stats_write
 21621-21635  _stimme_saubern
 21642-21666  _stimme_schon_gesagt
  9273-9289   _storage_cleanup_loop
 26389-26396  _story_for
  3778-3784   _stream_url_expiry
  3786-3791   _stream_url_ttl
 17032-17039  _streamer_persona_get
 22531-22689  _system_backup
 22698-22728  _system_backup_loop
 12660-12678  _task_auf_bot_schleife
 25138-25154  _telegram_befehlsmenue
  8316-8362   _telegram_polling_fehler
 25170-25205  _telegram_starten
  1492-1519   _telegram_ziele
 11614-11653  _test_proxy
 12036-12052  _testpush_resolve_live
 19735-19737  _text_schreiben
  7918-7926   _tg_botname
  7876-7915   _tg_ki_dialog
  9746-9756   _tg_migriert_laden
  9742-9743   _tg_migriert_pfad
  8611-8632   _tg_sprache_setzen
  9556-9566   _tg_topics_load_into_mem
  9553-9554   _tg_topics_path
  9568-9575   _tg_topics_save
 10923-10933  _token_ok
  9653-9669   _topic_anlegen
  9578-9585   _topic_forget
 13069-13080  _tracking_max_duration
  4783-4797   _tracking_remove_cleanup
  4814-4826   _tracking_resume_cleanup
  1868-1891   _try_attach_file_handler
 21611-21619  _tts_cleanup
 26049-26069  _tunnel_lage
 26210-26262  _tunnel_wacht_loop
 21114-21167  _twitch_channel_status
 24301-24449  _twitch_chat_loop
 23349-23362  _twitch_clip_versuchen
 24112-24218  _twitch_eventsub_loop
  1623-1643   _upload_queue_abarbeiten
  1470-1490   _upload_queue_add
  1588-1596   _upload_queue_count
  1646-1689   _upload_queue_eintrag
  1440-1444   _upload_queue_load
  1692-1718   _upload_queue_nachher
  1430-1432   _upload_queue_path
  1573-1577   _upload_queue_remove
  1464-1468   _upload_queue_save
  1447-1462   _upload_queue_schreibbar
  1580-1586   _upload_queue_update
 10144-10168  _upload_rest_sichern
  1598-1620   _upload_window_loop
  8122-8129   _uptime_s
 13270-13279  _url_host
  3452-3550   _url_nachschlag
   913-917    _usage_record_claude
 26502-26524  _v37_pause_source
 26466-26476  _v37_restream_restart
 26479-26499  _v37_unpause_source
  8534-8578   _verbindung_verloren
  7079-7110   _viewer_sample_loop
 11059-11062  _wants_html
  8132-8146   _warn_empty_env
 25856-25981  _watchdog_loop
 23833-23841  _wchat_thank_ok
 26177-26207  _werkzeug_wacht_loop
 18789-18827  _whisper_get_model
  8223-8231   _whisper_native_section
 17957-17963  _whisper_pool
 18921-18953  _whisper_segments
 18829-18845  _whisper_stumm
 18848-18918  _whisper_transcribe
 13751-13775  _write_restream_overlay
 13713-13748  _write_restream_overlay_async
 24473-24572  _youtube_api_chat_loop
 21170-21273  _youtube_api_status
 21276-21343  _youtube_channel_status
 24575-24741  _youtube_chat_loop
 23365-23390  _youtube_clip_versuchen
 23695-23708  _youtube_restream_autoconfig
 23711-23735  _youtube_restream_autoconfig_inner
 23802-23830  _youtube_send
 21407-21448  _youtube_set_channel
 23738-23772  _yt_access_token
 23775-23790  _yt_live_chat_id
 23798-23799  _yt_sendrate_cfg
 24452-24467  _yt_timeout
  3227-3228   _ytdlp_detect_available
  3243-3245   _ytdlp_einzeln
  3230-3241   _ytdlp_note_result
 12705-12707  _zombie_child_count
 25683-25700  _zustand_kennzahlen
  7998-8022   about
  4702-4706   add_ai_log_entry
  5091-5185   add_recording
  4758-4775   add_tracking
  6556-6589   ai
  4272-4369   ai_chat
  4468-4478   ai_history_append
  4480-4485   ai_history_clear
  4457-4466   ai_history_load
  4442-4455   ai_rate_limit_check
  6618-6626   aireset
 18320-18339  azrael_chat
 24746-24849  brain_cmd
  3794-3799   build_recording_cmd
  4778-4781   bulk_add_trackings
  7349-7408   bulkadd
  9420-9536   check_all_trackings
  4829-4841   claim_live_transition
 17125-17889  class KickModerator
 14766-16875  class RestreamManager
  5001-5002   class _AufnahmeLockVerloren
  8470-8531   class _KickClusterSuche
 11924-11966  classify_proxy_anonymity
  6664-6861   cleanup
  5554-5560   cleanup_old_recordings
  5026-5033   clear_recording
 23393-23414  clip_moment
  7471-7547   cookies_cmd
  7550-7593   cookies_datei_cmd
  4749-4755   count_trackings_for_chat
  4689-4700   decide_preferred_recorder
  6056-6203   diag
 25020-25081  einnahmen_cmd
  4650-4666   finish_recording_attempt
  4802-4804   get_all_active_trackings
  5187-5190   get_all_recordings
  4628-4631   get_archive_entry
  2374-2379   get_cookie_health
  5257-5263   get_event_log
  4673-4687   get_last_recording_attempt
  3553-3595   get_live_status
  5268-5271   get_priority_poll_interval
  4668-4671   get_recent_recording_attempts
  5192-5195   get_recording_by_id
  3961-3990   get_redis
  5548-5552   get_storage_stats
  5307-5309   get_tiktok_status_distribution
  4843-4852   get_tracking_state
  4799-4800   get_trackings_for_group
 10232-10700  handle_recording_finished
 25130-25135  hilfe_cmd
  4536-4601   init_db
  5830-5868   live
  8708-8738   live_check_worker
  4045-4092   llm_chat
  4202-4243   llm_chat_sync
  4187-4199   llm_list_models
  5216-5249   log_event
  1991-2024   log_recording_failure
  7743-7792   logs_cmd
 26998-27277  main
  6592-6615   on_ai_media
  7869-7873   on_ai_reply
  7981-7995   on_azrael_mention
  8027-8057   on_callback
  9801-9819   on_chat_migration
  7935-7948   on_link_video
 18345-18450  oracle_handle
  7632-7635   pause_tracking
  5603-5608   profile_keyboard
  5783-5827   quelle
  7694-7740   quota
  9196-9270   reaper_loop
  5303-5305   record_tiktok_status
  6631-6661   recstatus
  3992-4000   redis_get_json
  4003-4009   redis_set_json
 25157-25167  report_cmd
 11969-11971  report_proxy_result
  2635-2677   resolve_tiktok_live_stream
  7638-7641   resume_tracking
 25208-25461  run_bot
 12557-12651  run_flask
  4709-4715   save_tiktok_check
  5005-5024   set_recording_file
  4807-4811   set_tracking_paused
 25115-25127  spenden_cmd
  9825-9836   split_and_send_video
  5693-5735   start
  4634-4648   start_recording_attempt
  6864-6902   stats
  5472-5525   stop_manual_recording
  7644-7691   stoprec
  7003-7011   summary_cmd
  7795-7866   sysres
  6205-6349   teststream
  5737-5778   tiktok
  7411-7468   topusers
  5905-5962   track
  5870-5902   track_exact
  5987-6054   tracklist
  5336-5470   trigger_manual_recording
  4931-4966   try_acquire_recording_lock
 25084-25112  unpause_cmd
  5964-5985   untrack
 24904-25017  update_cmd
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
abwehrlage.py          auswerten, configure, crowdsec_status, crowdsec_via_lapi, cscli_bin, cscli_path, darf_journal_lesen, ssh_angriffe, sudo_hinweis
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, andere_kopien, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, dublette_loeschen, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, hat_quelle, run_archive_file_check, uebernehmen, unter_wurzel
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            aus_bestand, config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmechat.py        ass, ausschnitt, beenden, beginnen, clip_beginnt, clip_cmd, clip_fertig, clip_merken, clips_nehmen, clips_offen, concat_liste, einbrennen_cmd, laeuft, modus, notieren, untertitel_cmd, zusammenschnitt_cmd
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest, stall_grenze
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, ist_zieldatei, join_reste, luecken, probe_cmd, sekunden, sitzung_id, teildatei, tonformat, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelkontext.py       ausfall, block, fakten, letzte_erinnerung, nachricht, restream_quellen, sicher, streamer_waehlen
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_zugang, sys_backup, sys_hour, sys_keep
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
beobachtungsdienst.py  fuer_deck, grafana_jetzt, grafana_lage, grafana_unit, grund_text, installiert, prometheus_jetzt, prometheus_lage, selbstheilung_erlaubt, steuern
beobachtungslage.py    grafana, lage, prometheus
betriebslage.py        abschiedswache, bereit, bewerten, haengende_threads, sichern_beim_stopp
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            aendern, class FalscheForm, get, lesen, set_, upsert
channels.py            chat_anhaengen, chat_ausduennen, chat_eintraege, configure_chat, gehoert_in_kasten, letzte_zeit, quelle_aktiv, restream_active, yt_sendrate_cfg
chatbild.py            an, beenden, lage, starten
chatfolge.py           entscheide
chatnachtrag.py        beilage_lesen, beilage_zu, eingearbeitet, ensure_schema, erledigt, fehlversuch, ist_beilage, lesen, offene, stempel, unveraendert, vormerken
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
clientip.py            echte_ip, host_ist_lokal, ist_https, ist_lokal
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, bereinigen, class DateiGeaendert, class KeinDesktop, configure, desktop_pruefen, hole_gastcookies, schreibe, uebernehmen, zusammenfuehren
cookies.py             abgelaufen, auswahl, configure, gesundheit, hat_login, kritisch, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, gesetzte, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbgesundheit.py        messen
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, pruefen, vorbereiten
dbwartung.py           faellig_in, letzter_lauf, merken, stand_datei
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, mariadb_lage, set_pool, treiber_fehler, treiber_wunsch, vorrat_groesse, vorrat_lage, vorrat_leeren
dcspar.py              anzeige, client_optionen, puffer
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordaufnahme.py     an, an_alle, beschriftung, hochladen, teilen
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb, track_grenze_je_mitglied
discordrang.py         admin_rolle, admin_rolle_traegt, ist_eigentuemer, kanal_einwand, macht_rechte, rang_einwand, rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
discordziele.py        bereich_kanal_holen, bereich_name, bereiche_an, class KeinPlatz, clip_kanal, clip_kanal_des_bereichs, clip_kanal_holen, eigene_kanaele, einsortieren, gilde_waehlen, kanal_name, loeschbar, plan, platz, umzugsmarke, umzugsmarke_lesen, ziel_kanal
donations.py           configure, fmt_eur, kurse_aus_env, parse_number, summe_eur, to_eur, unknown_count, zeile_eur
donationsdb.py         manual_rows, manual_total, parse_eur
durchreicher.py        adresse, ist, main, nutzer_aus, werkzeug, werkzeuge, zieher_cmd, zieher_umgebung, zubringer_cmd
einstellungen.py       bekannt, class Abgelehnt, db_werte, geheim, gueltiger_name, in_umgebung_laden, katalog, pruefen, schutzgrund, setzen, startbericht, uebernehmen, uebersicht, zuruecksetzen
encodeschlange.py      lage, last_frei, parallel, platz, platz_sync
envdatei.py            class EnvdateiFehler, lesen, main, setzen, wert_lesen, wert_schreiben
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, schnappschuesse, schnappschuesse_kappen, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      anzeige_groesse, avatar_kette, chat_kasten, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
forkriegel.py          class Vortritt
freeai.py              abhilfe, alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
gegendruck.py          abgewiesen, deckel_auto, fd_grenze_anheben, fd_lage, freigeben, lage, reservieren, reserviert, start_entscheiden, verworfen, zuruecksetzen
geocache.py            anreichern, get, groesse, leeren, put
geoip.py               ist_privat, lookup
geschuetzt.py          lage, ruhend, vermerken, verschlossen, zuruecksetzen
heapzaum.py            arenen_wunsch, deckeln, lage, rss_mb, takt_min, zurueckgeben
herkunft.py            entscheiden
highlights.py          chat_raten, check, new_state, observe, score, zustand
httpsitzung.py         schliessen, sitzung, teilen
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          einwertig, prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, state_gueltig, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, naechster_cluster, naechster_key, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
kickzentrifugo.py      als_frame, antwort_fehler, class KickZentrifugoFehler, connect_cmd, fehler_code, ist_ping, kanal, lage, neue_client_id, neues_token, pause, refresh_cmd, subscribe_cmd, token_aus, ttl_aus, verbindung_body, ws_url_aus, zerlegen, zugang
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              azrael_lage, azrael_wahl, backend, beschriftung, brain_kette, deck_lage, deck_setzen, deck_wahl, etikett, gesamtzeit, herkunft, herkunft_loeschen, herkunft_setzen, herkunft_von, llm_zeiten, lokal_installiert, lokal_stand, lokal_zuerst, lokales_modell, normal, provider, vorrang, wartezeit, weg_zaehlen, zeitlimit
lagebild.py            bauen, dienst_quelle, dienste, dienste_lesen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
leitstand.py           bauen, drohnen, ereignis, ereignisse, kette, tafeln
linkvideo.py           abklingzeit_s, an, aufraeumen, ausgabe_lesen, befehl, bildunterschrift, configure, darf, grund, holen, ist_tiktok, links, max_dauer_s, sperre, werkzeug
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, schluessel, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           beste_url, braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
livemeldung.py         live_an, live_aus
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, einreihen, entkoppeln, nachziehen, schwaerzen, stoppen, synchrone_handler, verloren, wartend, zuruecksetzen
looplag.py             bremser, erfassen, lage, spaeher_starten, stelle_aus_rahmen, takt, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
mariadbumzug.py        class UmzugAbgebrochen, env_setzen, geoeffnet_von, in_benutzung, quelle_zaehlen, umziehen, vergleichen, ziel_zaehlen
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
mcpdienste.py          class Abgelehnt, class BestandUnbekannt, class Unbekannt, export, lage, liste, llama_adresse, loeschen, speichern, testen, webui
meldetakt.py           erfolg, gestoert, melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, sql_bedingung, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, aktive_agenten, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
oeffentlichestats.py   configure, public_stats
outcomes.py            get_outcome_breakdown
overlaybrowser.py      browser_cmd, class Dauerbrowser, class OverlayBrowserFehler, class SeiteNichtErreichbar, fifo_schreiben, lage, png_vollstaendig, teilen
overlaytext.py         alert_fuer, configure, follow_zeile, gehoert_zu, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok, overlay_url, quelle_zeile, reaktion_fuer, ziele
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
piperarbeiter.py       main
piperdienst.py         an, beenden, lage, sprechen
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
profildetail.py        datum, felder, kennzahlen, kontotyp, verlauf
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
prueflage.py           fuer_healthz, lage, merken, runde_gelaufen, uebersicht, vergessen
pruefschlange.py       erledigt, mit_frist, vorgemerkt, vormerken, zuruecksetzen
qrsvg.py               qr_svg
quellprobe.py          empfehlung, form, kurz, main, maske, messen, probe_durchreicher, probe_ffprobe, probe_html, probe_ytdlp, ttl
quellstat.py           lage, zaehlen, zuruecksetzen
raumkennung.py         grund, gueltig
raumsperre.py          deuten, faellig, lage, merken, snapshot, text, vergessen
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      abhilfe, class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, ein_start_je_ziel, fenstergroesse, freigeben, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, startend, url_host
restreamcfg.py         active_platforms, aktiv, bruecke, bruecke_luecke, bruecke_offline, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, chat_kasten, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, fueller, quell_eingang, schriftart, zubringer
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamliste.py       abgleichen, an, ausschliessen, zulassen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in, tiktok_geschenk
schema.py              anlegen, create_schema, index_sicher, kollation_angleichen, modultabellen, parameter, spalten_nachziehen
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
schriftzeichen.py      emoji_hinweis, emoji_pakete_fehlen, schrift_von, tabelle, vermutlich_unzeichenbar, vorbereiten, zeichenbar
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendebruecke.py        ausnahme_text, class Bruecke, class TsUmschreiber, ist_keyframe, pat_pmt_pid, pes_zeit, pid, pmt_stroeme, pmt_urteil, video_pid, weiche_grund
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          sicher_join, sicherer_name, unter
sicherungspruefung.py  archiv_lesbar, class DumpFehler, dump_vollstaendig, mysqldump, pruefen, schwaerzen
sitzungsschluessel.py  laden, pin_schluessel
speicherpflege.py      abgelaufene_weg, alte_stempel_weg, groessen
spendeninfo.py         krypto, paypal, paypal_url, stand, text
spendenziel.py         eingang, fenster_start, ist_monatlich, stand, summe, zeitraum, ziel_eur
sqldialekt.py          bei_konflikt
sqlguard.py            abbruch_nach, check_readonly, frist_ueberschritten, frist_unbekannt, mariadb_mit_frist, normalize, with_limit
sqlutil.py             zeitfenster_literal
stats.py               aufnahmen_je_tag, configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache, trefferquote
storage.py             class BestandUnbekannt, cleanup, forecast, notfall_raeumen, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
tagesbericht.py        bauen, configure
telegramfehler.py      dashboard_umzug, dauer_text, ersatz, grund, ist_fehler, ist_telegram_chat, migration_plan, migriert_erlaubt, nur_telegram, standardgruppe, start_endgueltig, start_pause, starten, text, zuruecksetzen
textmore.py            configure_banned_cap, pre_nachrichten, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tgantwort.py           angesprochen, echte_antwort, entscheiden, frage_ohne_namen, gemerkt, ist_brain_antwort, ist_ki_antwort, merken, ohne_brain_kopf, ohne_fuss
tgmarkdown.py          html_zu_md, teilen
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, garantie, garantie_cmd, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, empfaenger, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             ausfuehrbar_im_archiv, build_plan, check, class Plan, class UpdaterConfig, commit_zip_url, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, rechte_angleichen, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
uploadschlange.py      angekommen, beiseite, class SchlangeUnlesbar, faellig, gleicher, lesen, nach_versuch, pause_s
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, in_arbeit, ist_kaputter_container, ist_rest, kopier_teilen, neu_kodieren, platz_reicht, reparieren, teile, teile_entfernen, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, eigene_url, intern_basis, ist_loopback, schema, threads, tls_lage, waehle
werkzeugpfad.py        alter_tage, befund, lage, nachahmen_aus, pruefen, voranstellen
whispercfg.py          bedarf_mb, benutzt, entladen_wenn_leer, frei_mb, gebrauch, geladen, leerlauf_s, name, rss_hinweis, verfuegbar, waehle, wechsel_pruefen
youtube_api.py         active_broadcast_params, ban_payload, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlparbeiter.py       main
ytdlpdienst.py         alle_beenden, anzahl, ausfuehren, laeufe_max, lage
ytdlpurl.py            nur_frische, urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
zeitglaetter.py        ausdruck, bsf_args, filter_text, verfuegbar
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DatabaseAgent, class DiskAgent, class GrafanaAgent, class HealthAgent, class LearningAgent, class PrometheusAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime, ohne_denkblock
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler, frische_intervalle
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
