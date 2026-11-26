# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 11316  GET              /                                                dashboard
 12834  GET              /api/abo/status                                  api_abo_status
 12815  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11933  GET              /api/automation/status                           api_automation_status
 11955  POST             /api/automation/toggle                           api_automation_toggle
 21435  GET              /api/channel/categories                          api_channel_categories
 21441  POST             /api/channel/set                                 api_channel_set
 21292  GET              /api/channels/status                             api_channels_status
 20994  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20977  GET              /api/clips                                       api_clips
 21023  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20923  GET              /api/debug/threads                               api_debug_threads
 12820  GET              /api/events                                      api_events
 12311  GET              /api/events/stream                               api_events_stream
 12170  GET              /api/health                                      api_health
 20954  POST             /api/highlights/config                           api_highlights_config
 11246  POST             /api/login                                       dashboard_login_submit
 13052  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12240  GET              /api/notify/status                               api_notify_status
 12251  POST             /api/notify/test                                 api_notify_test
 12888  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12865  GET              /api/proxy/trend                                 api_proxy_trend
 21041  GET              /api/tts/<fn>                                    api_tts_file
 21818  GET              /api/upload_window                               api_upload_window
 12413  GET              /archive/<int:eid>/download                      archive_download
 12439  GET              /download/<int:recording_id>                     download
 12372  GET              /health                                          health
 20795  GET              /healthz                                         healthz
 11237  GET              /login                                           dashboard_login_page
 11271  GET              /logout                                          dashboard_logout
 11278  GET              /manifest.webmanifest                            pwa_manifest
 21799  GET              /overlay                                         overlay_page
 11302  GET              /pwa-icon-<variant>.png                          pwa_icon
 11288  GET              /sw.js                                           pwa_service_worker
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
  2723  /about                  Ueber diesen Bot
  1269  /ai                     
  2723  /aireset                KI-Kontext zuruecksetzen
  1714  /ask                    
  1370  /assign_role            
  1428  /ban                    
  2679  /botstats               
  2723  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2723  /bulkadd                Mehrere User auf einmal tracken · a b c
  2723  /cleanup                Alte Aufnahmen aufraeumen
  1987  /clearwarns             
  2643  /clip                   
  2628  /clipoftheweek          
  1850  /clips                  
  2723  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1325  /create_category        
  1296  /create_channel         
  1360  /create_group           
  1335  /create_role            
  1311  /create_voice           
  1591  /daily                  
  2723  /diag                   Vollstaendige Diagnose
  2723  /einnahmen              Einnahmen und Spenden
  1743  /event                  
  1785  /events                 
  1890  /follow                 
  1879  /help                   
  1416  /kick                   
  1563  /leaderboard            
  2723  /live                   Live-Status sofort pruefen · @user
  1837  /livenow                
  2723  /logs                   Letzte Fehler aus dem Log
  2723  /pause                  Tracking pausieren · @user
  1865  /post_test              
  1675  /profile                
  1454  /purge                  
  2723  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2723  /quota                  Speicher-Quota
  1550  /rank                   
  1825  /recstatus              
  1382  /remove_role            
  2723  /report                 Azrael-Sentinel-Wochenreport
  1282  /restream_status        
  2723  /resume                 Tracking fortsetzen · @user
  1394  /set_channel_perms      
  1514  /setup_community        
  1531  /setup_targets          
  1811  /spenden                
  1924  /stats                  
  1241  /status                 
  2723  /stoprec                Laufende Aufnahme sauber beenden · @user
  2025  /streaminfo             
  2723  /summary                Tageszusammenfassung
  2723  /sysres                 System-Ressourcen
  2723  /teststream             Recorder-Selbsttest · @user
  2723  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1440  /timeout                
  1997  /topstreamers           
  2723  /topusers               Top-Streamer nach Aufnahmen
  1150  /track                  
  2723  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
  1254  /tracklist              
  1906  /unfollow               
  2723  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
  1203  /untrack                
  1945  /warn                   
  1973  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2827  on_member_join
  2784  on_message
  2744  on_raw_reaction_add
  2864  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    59-74     konfiguriere
    77-543    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (70 Funktionen)

```
  2132-2183   _award_xp
  1468-1484   _bereiche_bericht
   557-568    _clip_kopieren
  2348-2377   _clip_week_leader
  2401-2412   _clipoftheweek_loop
   668-721    _clips_einsortieren
  2983-3047   _community_events_loop
   359-368    _dc_abbruch_melden
  2102-2108   _dc_bereit
  2059-2081   _dc_client
   342-356    _dc_fehlerart
  2084-2093   _dc_offen
  2111-2123   _dc_warten
  3087-3122   _disc_automod_check
   475-480    _disc_sprache_setzen
  2186-2234   _discord_ai_automod
   893-935    _discord_automod
  2237-2257   _discord_azrael_reply
  2547-2940   _discord_run_once
   249-326    _discord_start
   371-425    _ensure_discord_invite
  2946-2980   _ensure_error_channel
   504-517    _ensure_rank_roles
  1113-1127   _ensure_team_roles
  3050-3080   _error_channel_loop
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
  2510-2534   _stern_an_telegram
  2537-2544   _stern_anspruch_zurueck
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

## Top-Level-Symbole in bot.py (591 Funktionen, 4 Klassen)

```
 26660-26682  _abbruch_datenbank_unlesbar
  2845-2846   _abo_key
  2866-2884   _abo_probe_dump
 26782-26798  _abschied_wachen
 26801-26819  _abschluss
 17005-17012  _ad_allowlist
 18171-18177  _agent_for
 18180-18196  _ai_telemetry
 18712-18730  _alert
 22239-22289  _alert_monitor_loop
 19417-19474  _alte_beilagen_einsammeln
 22676-22738  _announce_loop
  3796-3806   _anthropic_key
  3809-3811   _anthropic_model
 10769-10772  _arg_int
  2837-2842   _as_dict
 26346-26355  _async_exc_handler
 18901-18923  _audio_tap_cmd
 19943-20002  _audio_tap_melden
 18937-18961  _audio_tap_sammler
 10116-10153  _aufnahme_beim_stopp_sichern
 19359-19380  _aufnahme_chat_ausklang
 19343-19356  _aufnahme_chat_beginnen
 19502-19523  _aufnahme_chat_dienst
 19701-19756  _aufnahme_chat_einarbeiten
 19338-19340  _aufnahme_chat_modus
 19526-19575  _aufnahme_chat_nachtrag
 19383-19414  _aufnahme_chat_vormerken
 19493-19499  _aufnahme_chat_wecken
 25462-25464  _aufnahme_deckel
 19578-19599  _aufnahme_fertigmachen
 22922-22983  _aufnahme_nach_discord
 10156-10174  _aufnahme_platz_frei
 10059-10086  _aufnahme_verteilen
 26746-26766  _aufnahmen_abschliessen
 26685-26743  _aufraeumen
 11058-11127  _auth_cookie
 11012-11054  _auth_guard
  2092-2097   _auto_on
 20658-20684  _auto_restream_loop
 14319-14361  _avatar_frames_laden
 17055-17068  _azrael_brain_kontext
 23896-23911  _azrael_broadcast_reply
 23796-23818  _azrael_chat_reply
 23768-23793  _azrael_chat_should_reply
 23824-23826  _azrael_gate_cfg
  4340-4355   _azrael_ki
 18199-18213  _azrael_live_state
  4358-4381   _azrael_lokal
 21685-21699  _azrael_overlay_state
 18255-18263  _azrael_persona_kern
 18594-18648  _azrael_proactive_loop
 18019-18075  _azrael_reaction_to_chats
 23829-23836  _azrael_reply_all_chats
  4384-4399   _azrael_schweigt_melden
 23755-23765  _azrael_self_names
 23864-23893  _azrael_send_to
 14280-14316  _azrael_spricht
 14638-14651  _azrael_stimme_stumm
 18219-18252  _azrael_system
 22373-22376  _backup_active
 22454-22467  _backup_loop
  5598-5621   _betreiber_pruefen
 25551-25555  _betrieb
 26419-26428  _brain_crowdsec_snap
 26587-26590  _brain_db_health
 24753-24793  _brain_fragen
 22160-22169  _brain_growth_loop
 11445-11472  _brain_growth_snapshot
  2756-2790   _brain_hint_delay
 26491-26526  _brain_moderation_snap
  6918-6946   _brain_notify
 26593-26615  _brain_recording_snap
 26431-26488  _brain_restream_health
 26618-26631  _brain_tiktok_status_snap
 12286-12307  _browser_push
 14685-14689  _build_restream_cmd
  5624-5651   _can_stop_tracking
  2203-2225   _capture_set_cookies
 12918-12921  _cfg_get
 12924-12926  _cfg_set
 21396-21431  _channel_set_all
 13361-13364  _chat_connected
 13367-13383  _chat_disconnected
 19487-19490  _chat_einarbeiten_async
  9550-9580   _chat_is_forum
 19307-19332  _chat_listener_abbauen
  9722-9757   _chat_migriert
  9760-9761   _chat_migriert_async
 13397-13399  _chat_sanitize
 13346-13358  _chat_stat
  4214-4226   _check_ai_models_sync
 11640-11683  _classify_pool_anonymity
   920-942    _claude_chat_sync_metered
 10814-10820  _client_ip
 23397-23411  _clip_chat_ass
 22822-22865  _clip_prune
 22868-22878  _clip_recfile_for
 23311-23385  _clip_schneiden
 23414-23420  _clip_should_velocity
 22986-23072  _clip_to_discord
 19672-19677  _clips_abwarten
  3996-4005   _close_ai_session
 23942-23957  _cohost_broadcast
 23927-23928  _cohost_cfg
 23983-23995  _cohost_fire_highlight
 23931-23939  _cohost_gate
 23960-23980  _cohost_highlight
  7248-7309   _cookie_alarm_loop
  2293-2294   _cookie_autofetch_info
  2277-2281   _cookie_autorefresh_info
 26016-26038  _cookie_bezug_loop
 26041-26066  _cookie_bezug_runde
  2180-2184   _cookie_header
 10823-10828  _cookie_sicher
  2306-2320   _cookies_selbst_holen
  4489-4491   _create_index_safe
  7134-7161   _daily_summary_loop
  3322-3347   _darf_ytdlp_nachschlagen
 12454-12475  _dashboard_adresse
 10843-10847  _dashboard_hostnamen
  1536-1566   _dashboard_trackings_umziehen
 23388-23394  _datei_weg
 22213-22236  _db_maintenance_loop
  7084-7131   _db_vacuum_loop
 12478-12487  _deck_intern_url
 17028-17052  _detect_foreign_ad
  1773-1784   _diag_path_owner
 18499-18544  _director_finalize
 19933-19940  _director_for
 18448-18496  _director_mark
 23224-23227  _disc_state_get
 23230-23237  _disc_state_set
 22141-22150  _discord_bot_starten
 22104-22115  _discord_einladung_merken
 22153-22157  _discord_invite
 22118-22138  _discord_kontext
 23185-23221  _discord_live_thread
 18651-18663  _discord_notify
 22076-22101  _discord_ops_alert
 23083-23181  _discord_post_user
 22741-22747  _discord_stop
  7164-7245   _disk_alarm_loop
 25887-25938  _disk_autoclean
 26202-26215  _disk_guard_loop
 14259-14266  _drossel_hoeher
 14255-14256  _drossel_stufe
 14269-14277  _drossel_zuruecksetzen
 12656-12658  _dump_all_threads
 25558-25572  _einstellungen_startzeile
  2345-2406   _ensure_cookie_file_netscape
  9651-9654   _ensure_notify_topic
 11790-11827  _ensure_proxy_ready
  9590-9613   _ensure_topic
   763-765    _env_int
   768-770    _env_int_range
 18696-18709  _event_webhook
 13144-13157  _evolution_loop
  6324-6358   _extract_file_payload
  1522-1533   _fanout_ziele
 26822-26887  _fatal_vom_botteil
 25467-25482  _fd_grenze_anheben
  5166-5176   _fehler_text
 11539-11557  _fetch_proxy_list
 19276-19304  _fetch_tiktok_room_id
   848-851    _ff_cmd
 19685-19698  _ffprobe_masse
 14183-14199  _fifo_schreiber_wecken
 13971-13976  _find_chromium
  3717-3719   _find_external_recorder
  2469-2471   _find_stream_urls
 12967-12992  _fire_webhooks
  8197-8207   _fork_safe
   953-966    _freeai_chat_sync_metered
  3984-3993   _get_ai_session
  8025-8065   _get_live_info
  3166-3173   _get_resolve_semaphore
  8722-9157   _handle_single_tracking
 25671-25673  _hb
 25676-25693  _hb_while
 20908-20919  _healthz_fuer_aufrufer
 25717-25745  _heap_zurueckgeben
 11131-11148  _herkunft_guard
 13411-13413  _highlight_cfg
 13416-13445  _highlight_observe
 12490-12500  _htmlov_basis_url
 14043-14051  _htmlov_bild_schreiben
 14012-14040  _htmlov_dauerbrowser
 13991-14009  _htmlov_screenshot_cmd
 13979-13988  _htmlov_url
 18963-18973  _httpx_proxy
 13000-13012  _in_quiet_hours
 26646-26657  _init_db_oder_abbruch
 27501-27532  _install_fast_eventloop
 10664-10718  _install_fast_json
 12661-12677  _install_faulthandler
 20704-20713  _intel_ensure_schema
 20756-20791  _intel_index_loop
 20725-20740  _intel_index_one
 20716-20722  _intel_semantic
  5576-5596   _is_authorized
  8548-8569   _is_dead
  1992-1999   _is_process_running
  6948-6955   _is_quiet_hours
  1411-1420   _is_upload_window
  4998-5013   _iso
 10831-10840  _ist_lokal
 10753-10766  _json_error_handler
  4058-4077   _ki_nach_deckwahl
  4135-4144   _ki_rueckfall_melden
  8423-8430   _kick_cluster_gefunden
  8358-8420   _kick_cluster_weiter
  6997-7039   _kick_follower_count
  6981-6984   _kick_slug
  8328-8355   _kick_ws_pause
 26634-26643  _kickmod_boot
 25982-25985  _lagebild_discord_aufnahme
 25995-25999  _lagebild_kick_chat
 25988-25992  _lagebild_overlay
 26002-26004  _lagebild_spendenziel
 25969-25979  _lagebild_upload
 13029-13031  _latest_popularity
  1929-1938   _laufstand
 26157-26199  _laufstand_loop
 25595-25633  _leistung_erheben
  7914-7941   _link_video_senden
  8709-8720   _live_check_frist_melden
  2900-2913   _live_ohne_stream
 20341-20390  _live_react_loop
 20005-20327  _live_react_worker
  3565-3679   _live_status_aufloesen
 18078-18089  _live_transcript_push
 20329-20339  _live_users
 18547-18591  _living_title_loop
 22379-22451  _local_backup_scan
  4932-4961   _lock_update
 10735-10749  _log_5xx
 25636-25668  _log_schleuse_pruefen
   838-845    _log_sicher
 14697-14709  _looks_like_codec_err
 14692-14694  _looks_like_source_expired
  8246-8276   _loop_fehler
 12680-12689  _loop_heartbeat
 25373-25406  _loop_lag_monitor
 25420-25440  _loop_stockung_melden
 25443-25453  _loop_takt_starten
 12692-12765  _loop_watchdog_thread
 17955-17972  _loyalty_add
 17946-17952  _loyalty_get
 17975-17983  _loyalty_top
  5277-5296   _manual_status
  8571-8572   _mark_dead
 12010-12026  _marketing_loop
 23843-23861  _maybe_handle_command
 26301-26325  _maybe_hype_clip
 22791-22819  _meme_klassifizieren
 19602-19669  _meme_zusammenschnitt
  4476-4481   _migrate_columns
 24125-24136  _mod_is_exempt
 24139-24144  _mod_warn_first
 24147-24150  _mod_warn_text
 13186-13205  _modlog
 13169-13183  _modlog_schreiben
  1104-1106   _multistream_targets
  3350-3386   _nachschlag_ytdlp
  8210-8211   _nc_create_subprocess_exec
  8214-8215   _nc_create_subprocess_shell
 12124-12141  _news_loop
 13228-13230  _normalize_ingest
  2687-2704   _note_check_duration
  9645-9648   _notify_topic_name
  4080-4085   _nur_free
  4088-4092   _nur_free_sync
  4095-4132   _nur_lokal_sync
  2891-2897   _offline_ergebnis
  3389-3412   _ohne_url_melden
 18104-18112  _oracle_memories
 18399-18433  _oracle_memorize
 18115-18128  _oracle_persona
 18097-18101  _oracle_recent_text
 13634-13635  _ov_atomic_write
 13625-13627  _ov_bar
 16933-16945  _ov_clip_text
 13630-13631  _ov_oneline
 13724-13785  _overlay_kanalweit
 21734-21792  _overlay_push
 13925-13968  _overlay_render_size
 13788-13815  _overlay_sendebild_schreiben
 13297-13301  _overlay_session_reset
 21701-21703  _overlay_src_ok
 13644-13656  _overlay_takt
 17015-17025  _own_invites
 13920-13922  _parse_size
  7559-7592   _pause_resume_cmd
  2231-2275   _persist_refreshed_cookies
  2134-2166   _pick_checked_pull_proxy
 10897-10912  _pin_auth_value
 11001-11002  _pin_clear_fail
 10965-10968  _pin_global_gesperrt
 10918-10929  _pin_hmac_schluessel
 10971-10978  _pin_locked
 10981-10998  _pin_note_fail
 10932-10953  _pin_ok
 21529-21554  _piper_pick_model
 21614-21679  _piper_say
 12929-12964  _post_json_threaded
 13899-13917  _probe_video_size
  2020-2037   _proc_is_recorder
 11759-11787  _proxy_pool_refresh_loop
  2100-2131   _proxy_report_recording
  9296-9380   _pruef_runde
  9255-9293   _pruefstand_melden
 25502-25513  _pruefung_verworfen
 12646-12648  _prune_stall_dumps
  2297-2303   _pull_proxy_still
 18667-18693  _push_notify
 11195-11197  _pwa_dir
 11608-11625  _quick_validate_proxy
 12995-12997  _quiet_hours_config
 11160-11193  _rate_guard
  2916-2944   _raumsperre_fragen
 17916-17922  _react_warn
  8112-8151   _reap_proc
 10850-10866  _rebinding_melden
  9989-10056  _rec_auto_abschalten
  9936-9986   _rec_frueh_getrennt
  9801-9881   _rec_kategorie_melden
  9884-9933   _rec_totstreak_fortschreiben
  2727-2749   _record_check_outcome
   833-835    _redact_stream_urls
 11686-11756  _refresh_proxy_pool
  2504-2595   _resolve_via_html
  2947-3143   _resolve_via_webcast_api_v2
  3211-3298   _resolve_via_ytdlp
 23454-23583  _resolve_youtube_ingest
  2480-2501   _resolver_stumm
 13280-13291  _restream_active_sources
 14364-14502  _restream_avatar_feeder_start
 14505-14515  _restream_avatar_feeder_stop
 19759-19897  _restream_chat_guardian
 13448-13533  _restream_chat_push
 13610-13620  _restream_chat_push_async
 14202-14219  _restream_chatbild_start
 26529-26584  _restream_durchreicher
 14054-14180  _restream_html_overlay_start
 14222-14242  _restream_html_overlay_stop
 20642-20655  _restream_liste_abgleichen
 13239-13262  _restream_overlay_files
 20393-20425  _restream_platform_state
 20601-20636  _restream_resume_after_restart
 13564-13581  _restream_soll_schreiben
 13584-13607  _restream_status_schreiben
 14563-14635  _restream_tts_enqueue_wav
 13861-13893  _restream_tts_feeder
 13858-13859  _restream_tts_fifo_path
 14518-14545  _restream_tts_start
 14547-14561  _restream_tts_stop
 20431-20598  _restream_verify_loop
 22344-22356  _retention_loop
 22338-22341  _retention_scan
  2848-2850   _room_is_abo
  6361-6516   _run_ai_call
 12788-12801  _run_async_from_flask
 27490-27498  _run_selfcheck_and_exit
 22359-22370  _s3_client
  8598-8668   _safe_send
  5240-5256   _sample_net_throughput
 27470-27487  _sc_bericht
 27411-27467  _sc_dienste
 27318-27408  _sc_ki_und_stimme
 27269-27315  _sc_umgebung
  2793-2823   _schedule_next_check
 22292-22335  _scheduler_loop
  4484-4486   _schema_pk
 12804-12809  _scraper_session
 24153-24192  _screen_full
 12186-12223  _sec_headers
  2464-2466   _select_stream_from_data_section
 27179-27266  _selfcheck
  9657-9691   _send_live_notice
  1434-1438   _should_defer_upload
 22881-22919  _shrink_for_discord
 11200-11233  _sicheres_ziel
 22172-22210  _sicherheits_erinnerung_loop
 26222-26239  _sign_health_check
 26242-26261  _sign_health_loop
  5016-5046   _sitzung_bestimmen
 20891-20901  _sparen_lage
  8227-8238   _spawn
 27923-27953  _spawn_from_flask
 25516-25522  _speicher_maps
 25525-25540  _speicher_pflegen
 18975-19273  _start_chat_listener
 25485-25499  _start_gesperrt
 12768-12785  _start_loop_watchdog
 12072-12121  _stats_loop
 12051-12054  _stats_output_path
 12057-12069  _stats_write
 21566-21580  _stimme_saubern
 21587-21611  _stimme_schon_gesagt
  9236-9252   _storage_cleanup_loop
 26281-26288  _story_for
  3741-3747   _stream_url_expiry
  3749-3754   _stream_url_ttl
 16978-16985  _streamer_persona_get
 22476-22634  _system_backup
 22643-22673  _system_backup_loop
 12606-12624  _task_auf_bot_schleife
 25030-25046  _telegram_befehlsmenue
  8279-8325   _telegram_polling_fehler
 25062-25097  _telegram_starten
  1492-1519   _telegram_ziele
 11560-11599  _test_proxy
 11982-11998  _testpush_resolve_live
 19680-19682  _text_schreiben
  7881-7889   _tg_botname
  7839-7878   _tg_ki_dialog
  9709-9719   _tg_migriert_laden
  9705-9706   _tg_migriert_pfad
  8574-8595   _tg_sprache_setzen
  9519-9529   _tg_topics_load_into_mem
  9516-9517   _tg_topics_path
  9531-9538   _tg_topics_save
 10869-10879  _token_ok
  9616-9632   _topic_anlegen
  9541-9548   _topic_forget
 13015-13026  _tracking_max_duration
  4746-4760   _tracking_remove_cleanup
  4777-4789   _tracking_resume_cleanup
  1831-1854   _try_attach_file_handler
 21556-21564  _tts_cleanup
 25941-25961  _tunnel_lage
 26102-26154  _tunnel_wacht_loop
 21059-21112  _twitch_channel_status
 24195-24343  _twitch_chat_loop
 23243-23256  _twitch_clip_versuchen
 24006-24112  _twitch_eventsub_loop
  1619-1656   _upload_queue_abarbeiten
  1470-1490   _upload_queue_add
  1584-1592   _upload_queue_count
  1440-1444   _upload_queue_load
  1659-1681   _upload_queue_nachher
  1430-1432   _upload_queue_path
  1569-1573   _upload_queue_remove
  1464-1468   _upload_queue_save
  1447-1462   _upload_queue_schreibbar
  1576-1582   _upload_queue_update
 10089-10113  _upload_rest_sichern
  1594-1616   _upload_window_loop
  8085-8092   _uptime_s
 13216-13225  _url_host
  3415-3513   _url_nachschlag
   913-917    _usage_record_claude
 26394-26416  _v37_pause_source
 26358-26368  _v37_restream_restart
 26371-26391  _v37_unpause_source
  8497-8541   _verbindung_verloren
  7042-7073   _viewer_sample_loop
 11005-11008  _wants_html
  8095-8109   _warn_empty_env
 25748-25873  _watchdog_loop
 23727-23735  _wchat_thank_ok
 26069-26099  _werkzeug_wacht_loop
 18735-18773  _whisper_get_model
  8186-8194   _whisper_native_section
 17903-17909  _whisper_pool
 18867-18899  _whisper_segments
 18775-18791  _whisper_stumm
 18794-18864  _whisper_transcribe
 13697-13721  _write_restream_overlay
 13659-13694  _write_restream_overlay_async
 24367-24466  _youtube_api_chat_loop
 21115-21218  _youtube_api_status
 21221-21288  _youtube_channel_status
 24469-24633  _youtube_chat_loop
 23259-23284  _youtube_clip_versuchen
 23589-23602  _youtube_restream_autoconfig
 23605-23629  _youtube_restream_autoconfig_inner
 23696-23724  _youtube_send
 21352-21393  _youtube_set_channel
 23632-23666  _yt_access_token
 23669-23684  _yt_live_chat_id
 23692-23693  _yt_sendrate_cfg
 24346-24361  _yt_timeout
  3190-3191   _ytdlp_detect_available
  3206-3208   _ytdlp_einzeln
  3193-3204   _ytdlp_note_result
 12651-12653  _zombie_child_count
 25575-25592  _zustand_kennzahlen
  7961-7985   about
  4665-4669   add_ai_log_entry
  5054-5148   add_recording
  4721-4738   add_tracking
  6519-6552   ai
  4235-4332   ai_chat
  4431-4441   ai_history_append
  4443-4448   ai_history_clear
  4420-4429   ai_history_load
  4405-4418   ai_rate_limit_check
  6581-6589   aireset
 18266-18285  azrael_chat
 24638-24741  brain_cmd
  3757-3762   build_recording_cmd
  4741-4744   bulk_add_trackings
  7312-7371   bulkadd
  9383-9499   check_all_trackings
  4792-4804   claim_live_transition
 17071-17835  class KickModerator
 14712-16821  class RestreamManager
  4964-4965   class _AufnahmeLockVerloren
  8433-8494   class _KickClusterSuche
 11870-11912  classify_proxy_anonymity
  6627-6824   cleanup
  5517-5523   cleanup_old_recordings
  4989-4996   clear_recording
 23287-23308  clip_moment
  7434-7510   cookies_cmd
  7513-7556   cookies_datei_cmd
  4712-4718   count_trackings_for_chat
  4652-4663   decide_preferred_recorder
  6019-6166   diag
 24912-24973  einnahmen_cmd
  4613-4629   finish_recording_attempt
  4765-4767   get_all_active_trackings
  5150-5153   get_all_recordings
  4591-4594   get_archive_entry
  2337-2342   get_cookie_health
  5220-5226   get_event_log
  4636-4650   get_last_recording_attempt
  3516-3558   get_live_status
  5231-5234   get_priority_poll_interval
  4631-4634   get_recent_recording_attempts
  5155-5158   get_recording_by_id
  3924-3953   get_redis
  5511-5515   get_storage_stats
  5270-5272   get_tiktok_status_distribution
  4806-4815   get_tracking_state
  4762-4763   get_trackings_for_group
 10177-10646  handle_recording_finished
 25022-25027  hilfe_cmd
  4499-4564   init_db
  5793-5831   live
  8671-8701   live_check_worker
  4008-4055   llm_chat
  4165-4206   llm_chat_sync
  4150-4162   llm_list_models
  5179-5212   log_event
  1954-1987   log_recording_failure
  7706-7755   logs_cmd
 26890-27169  main
  6555-6578   on_ai_media
  7832-7836   on_ai_reply
  7944-7958   on_azrael_mention
  7990-8020   on_callback
  9764-9782   on_chat_migration
  7898-7911   on_link_video
 18291-18396  oracle_handle
  7595-7598   pause_tracking
  5566-5571   profile_keyboard
  5746-5790   quelle
  7657-7703   quota
  9159-9233   reaper_loop
  5266-5268   record_tiktok_status
  6594-6624   recstatus
  3955-3963   redis_get_json
  3966-3972   redis_set_json
 25049-25059  report_cmd
 11915-11917  report_proxy_result
  2598-2640   resolve_tiktok_live_stream
  7601-7604   resume_tracking
 25100-25353  run_bot
 12503-12597  run_flask
  4672-4678   save_tiktok_check
  4968-4987   set_recording_file
  4770-4774   set_tracking_paused
 25007-25019  spenden_cmd
  9788-9799   split_and_send_video
  5656-5698   start
  4597-4611   start_recording_attempt
  6827-6865   stats
  5435-5488   stop_manual_recording
  7607-7654   stoprec
  6966-6974   summary_cmd
  7758-7829   sysres
  6168-6312   teststream
  5700-5741   tiktok
  7374-7431   topusers
  5868-5925   track
  5833-5865   track_exact
  5950-6017   tracklist
  5299-5433   trigger_manual_recording
  4894-4929   try_acquire_recording_lock
 24976-25004  unpause_cmd
  5927-5948   untrack
 24796-24909  update_cmd
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
discordaufnahme.py     an, beschriftung, hochladen, teilen
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
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
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
