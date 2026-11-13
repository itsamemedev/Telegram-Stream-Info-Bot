# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 11161  GET              /                                                dashboard
 12654  GET              /api/abo/status                                  api_abo_status
 12635  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11778  GET              /api/automation/status                           api_automation_status
 11800  POST             /api/automation/toggle                           api_automation_toggle
 21104  GET              /api/channel/categories                          api_channel_categories
 21110  POST             /api/channel/set                                 api_channel_set
 20961  GET              /api/channels/status                             api_channels_status
 20663  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20646  GET              /api/clips                                       api_clips
 20692  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20592  GET              /api/debug/threads                               api_debug_threads
 12640  GET              /api/events                                      api_events
 12156  GET              /api/events/stream                               api_events_stream
 12015  GET              /api/health                                      api_health
 20623  POST             /api/highlights/config                           api_highlights_config
 11091  POST             /api/login                                       dashboard_login_submit
 12872  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12085  GET              /api/notify/status                               api_notify_status
 12096  POST             /api/notify/test                                 api_notify_test
 12708  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12685  GET              /api/proxy/trend                                 api_proxy_trend
 20710  GET              /api/tts/<fn>                                    api_tts_file
 21458  GET              /api/upload_window                               api_upload_window
 12258  GET              /archive/<int:eid>/download                      archive_download
 12284  GET              /download/<int:recording_id>                     download
 12217  GET              /health                                          health
 20464  GET              /healthz                                         healthz
 11082  GET              /login                                           dashboard_login_page
 11116  GET              /logout                                          dashboard_logout
 11123  GET              /manifest.webmanifest                            pwa_manifest
 21439  GET              /overlay                                         overlay_page
 11147  GET              /pwa-icon-<variant>.png                          pwa_icon
 11133  GET              /sw.js                                           pwa_service_worker
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
   504  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   768  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   650  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   633  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   625  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   812  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   777  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   797  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   684  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
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
   446  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   431  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   251  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   186  POST             /api/cookies/bereinigen                          api_cookies_bereinigen   [nc/routes/settings.py]
   131  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    72  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    79  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   496  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   272  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   299  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   392  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   336  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   354  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   259  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
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
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   125  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   139  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   154  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
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
   222  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   242  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   269  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
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
   259  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   242  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
   151  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   268  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   590  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   565  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   964  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1086  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1114  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1134  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   951  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1013  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1000  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   981  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   626  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   621  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   669  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   552  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   879  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   643  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   606  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   579  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   853  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   723  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   812  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   718  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   651  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   442  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   896  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   530  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   774  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   929  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   914  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   486  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   713  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   699  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   682  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   739  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1277  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1398  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1241  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   832  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   728  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
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
   487  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   477  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   517  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
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
   237  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   458  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   487  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   407  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   420  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   516  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   393  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   268  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   337  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   324  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   164  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   282  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   133  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   374  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   429  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
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
   126  GET              /overlay/chat                                    overlay_chatbild   [nc/routes/overlay.py]
   141  GET              /overlay/chat.json                               overlay_chatbild_daten   [nc/routes/overlay.py]
```

## Discord-Slash-Commands in discordbot.py (67)

```
  2231  /about                  Ueber diesen Bot
   968  /ai                     
  2231  /aireset                KI-Kontext zuruecksetzen
  1383  /ask                    
  1069  /assign_role            
  1119  /ban                    
  2187  /botstats               
  2231  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2231  /bulkadd                Mehrere User auf einmal tracken · a b c
  2231  /cleanup                Alte Aufnahmen aufraeumen
  1649  /clearwarns             
  2151  /clip                   
  2136  /clipoftheweek          
  1519  /clips                  
  2231  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1024  /create_category        
   995  /create_channel         
  1059  /create_group           
  1034  /create_role            
  1010  /create_voice           
  1260  /daily                  
  2231  /diag                   Vollstaendige Diagnose
  2231  /einnahmen              Einnahmen und Spenden
  1412  /event                  
  1454  /events                 
  1559  /follow                 
  1548  /help                   
  1109  /kick                   
  1232  /leaderboard            
  2231  /live                   Live-Status sofort pruefen · @user
  1506  /livenow                
  2231  /logs                   Letzte Fehler aus dem Log
  2231  /pause                  Tracking pausieren · @user
  1534  /post_test              
  1344  /profile                
  1141  /purge                  
  2231  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2231  /quota                  Speicher-Quota
  1219  /rank                   
  1494  /recstatus              
  1079  /remove_role            
  2231  /report                 Azrael-Sentinel-Wochenreport
   981  /restream_status        
  2231  /resume                 Tracking fortsetzen · @user
  1089  /set_channel_perms      
  1181  /setup_community        
  1198  /setup_targets          
  1480  /spenden                
  1591  /stats                  
   940  /status                 
  2231  /stoprec                Laufende Aufnahme sauber beenden · @user
  1687  /streaminfo             
  2231  /summary                Tageszusammenfassung
  2231  /sysres                 System-Ressourcen
  2231  /teststream             Recorder-Selbsttest · @user
  2231  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1129  /timeout                
  1659  /topstreamers           
  2231  /topusers               Top-Streamer nach Aufnahmen
   870  /track                  
  2231  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   953  /tracklist              
  1573  /unfollow               
  2231  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   902  /untrack                
  1612  /warn                   
  1635  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2398  on_member_join
  2355  on_message
  2252  on_raw_reaction_add
  2433  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    60-75     konfiguriere
    78-533    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (53 Funktionen)

```
  1764-1815   _award_xp
   537-564    _bereich_umziehen
   484-494    _clip_kopieren
  1986-2015   _clip_week_leader
  2039-2053   _clipoftheweek_loop
  2550-2612   _community_events_loop
  1721-1743   _dc_client
  1746-1755   _dc_offen
  2652-2687   _disc_automod_check
   410-415    _disc_sprache_setzen
  1818-1866   _discord_ai_automod
   673-712    _discord_automod
  1869-1889   _discord_azrael_reply
  2056-2509   _discord_run_once
   245-303    _discord_start
   306-360    _ensure_discord_invite
  2515-2547   _ensure_error_channel
   431-444    _ensure_rank_roles
   833-847    _ensure_team_roles
  2615-2645   _error_channel_loop
   722-726    _guard
   642-670    _handle_voice_ai
   418-428    _is_admin
   509-534    _link_video
  1934-1945   _liveboard_loop
   729-762    _on_level_up
   638-639    _par_chat_id
  2018-2036   _post_clip_of_week
  1948-1966   _post_weekly_digest
   447-473    _provision_base_channels
  1486-1580   _reg_betrieb
  1155-1249   _reg_community_setup
  1252-1333   _reg_daily_profil
  1376-1473   _reg_frage_events
   927-983    _reg_info
  1101-1152   _reg_moderation
  1336-1373   _reg_profil
  1050-1098   _reg_rollen
   986-1047   _reg_server
  1476-1483   _reg_spenden
  1583-1670   _reg_streamer
  1673-1718   _reg_system
   861-924    _reg_tracking
   797-830    _run_tg_handler
   162-224    _uebernehmen
   497-506    _umzugsmarken
  1898-1931   _update_liveboard
  1969-1983   _weekly_digest_loop
   476-481    _ziel_guild
   567-609    _ziele_abgleichen
   618-635    _ziele_sync_loop
   612-615    _ziele_takt_min
   227-230    starte
```

## Top-Level-Symbole in bot.py (584 Funktionen, 4 Klassen)

```
 26231-26253  _abbruch_datenbank_unlesbar
  2820-2821   _abo_key
  2841-2859   _abo_probe_dump
 26353-26369  _abschied_wachen
 26372-26390  _abschluss
 16677-16684  _ad_allowlist
 17843-17849  _agent_for
 17852-17868  _ai_telemetry
 18384-18402  _alert
 21876-21926  _alert_monitor_loop
 19089-19146  _alte_beilagen_einsammeln
 22307-22369  _announce_loop
  3771-3781   _anthropic_key
  3784-3786   _anthropic_model
 10650-10653  _arg_int
  2812-2817   _as_dict
 25917-25926  _async_exc_handler
 18573-18595  _audio_tap_cmd
 19615-19674  _audio_tap_melden
 18609-18633  _audio_tap_sammler
  9999-10036  _aufnahme_beim_stopp_sichern
 19031-19052  _aufnahme_chat_ausklang
 19015-19028  _aufnahme_chat_beginnen
 19174-19195  _aufnahme_chat_dienst
 19373-19428  _aufnahme_chat_einarbeiten
 19010-19012  _aufnahme_chat_modus
 19198-19247  _aufnahme_chat_nachtrag
 19055-19086  _aufnahme_chat_vormerken
 19165-19171  _aufnahme_chat_wecken
 25042-25044  _aufnahme_deckel
 19250-19271  _aufnahme_fertigmachen
 22544-22597  _aufnahme_nach_discord
 10039-10057  _aufnahme_platz_frei
  9942-9969   _aufnahme_verteilen
 26317-26337  _aufnahmen_abschliessen
 26256-26314  _aufraeumen
 10924-10993  _auth_cookie
 10880-10920  _auth_guard
  2067-2072   _auto_on
 20327-20353  _auto_restream_loop
 14142-14184  _avatar_frames_laden
 16727-16740  _azrael_brain_kontext
 23501-23516  _azrael_broadcast_reply
 23401-23423  _azrael_chat_reply
 23373-23398  _azrael_chat_should_reply
 23429-23431  _azrael_gate_cfg
  4315-4330   _azrael_ki
 17871-17885  _azrael_live_state
  4333-4356   _azrael_lokal
 21354-21368  _azrael_overlay_state
 17927-17935  _azrael_persona_kern
 18266-18320  _azrael_proactive_loop
 17691-17747  _azrael_reaction_to_chats
 23434-23441  _azrael_reply_all_chats
  4359-4374   _azrael_schweigt_melden
 23360-23370  _azrael_self_names
 23469-23498  _azrael_send_to
 14103-14139  _azrael_spricht
 14450-14463  _azrael_stimme_stumm
 17891-17924  _azrael_system
 22010-22013  _backup_active
 22091-22104  _backup_loop
  5507-5530   _betreiber_pruefen
 25131-25135  _betrieb
 25990-25999  _brain_crowdsec_snap
 26158-26161  _brain_db_health
 24358-24398  _brain_fragen
 21797-21806  _brain_growth_loop
 11290-11317  _brain_growth_snapshot
  2731-2765   _brain_hint_delay
 26062-26097  _brain_moderation_snap
  6818-6846   _brain_notify
 26164-26186  _brain_recording_snap
 26002-26059  _brain_restream_health
 26189-26202  _brain_tiktok_status_snap
 12131-12152  _browser_push
 14497-14501  _build_restream_cmd
  5533-5560   _can_stop_tracking
  2178-2200   _capture_set_cookies
 12738-12741  _cfg_get
 12744-12746  _cfg_set
 21065-21100  _channel_set_all
 13181-13184  _chat_connected
 13187-13203  _chat_disconnected
 19159-19162  _chat_einarbeiten_async
  9433-9463   _chat_is_forum
 18979-19004  _chat_listener_abbauen
  9605-9640   _chat_migriert
  9643-9644   _chat_migriert_async
 13217-13219  _chat_sanitize
 13166-13178  _chat_stat
  4189-4201   _check_ai_models_sync
 11485-11528  _classify_pool_anonymity
   920-942    _claude_chat_sync_metered
 10682-10688  _client_ip
 23002-23016  _clip_chat_ass
 22453-22487  _clip_prune
 22490-22500  _clip_recfile_for
 22922-22990  _clip_schneiden
 23019-23025  _clip_should_velocity
 22600-22685  _clip_to_discord
 19344-19349  _clips_abwarten
  3971-3980   _close_ai_session
 23547-23562  _cohost_broadcast
 23532-23533  _cohost_cfg
 23588-23600  _cohost_fire_highlight
 23536-23544  _cohost_gate
 23565-23585  _cohost_highlight
  7148-7209   _cookie_alarm_loop
  2268-2269   _cookie_autofetch_info
  2252-2256   _cookie_autorefresh_info
 25592-25614  _cookie_bezug_loop
 25617-25642  _cookie_bezug_runde
  2155-2159   _cookie_header
 10691-10696  _cookie_sicher
  2281-2295   _cookies_selbst_holen
  4464-4466   _create_index_safe
  7034-7061   _daily_summary_loop
  3297-3322   _darf_ytdlp_nachschlagen
 12299-12320  _dashboard_adresse
 10711-10715  _dashboard_hostnamen
  1520-1550   _dashboard_trackings_umziehen
 22993-22999  _datei_weg
 21850-21873  _db_maintenance_loop
  6984-7031   _db_vacuum_loop
 16700-16724  _detect_foreign_ad
  1748-1759   _diag_path_owner
 18171-18216  _director_finalize
 19605-19612  _director_for
 18120-18168  _director_mark
 22835-22838  _disc_state_get
 22841-22848  _disc_state_set
 21778-21787  _discord_bot_starten
 21741-21752  _discord_einladung_merken
 21790-21794  _discord_invite
 21755-21775  _discord_kontext
 22796-22832  _discord_live_thread
 18323-18335  _discord_notify
 21713-21738  _discord_ops_alert
 22696-22792  _discord_post_user
 22372-22378  _discord_stop
  7064-7145   _disk_alarm_loop
 25463-25514  _disk_autoclean
 25773-25786  _disk_guard_loop
 14082-14089  _drossel_hoeher
 14078-14079  _drossel_stufe
 14092-14100  _drossel_zuruecksetzen
 12476-12478  _dump_all_threads
 25138-25152  _einstellungen_startzeile
  2320-2381   _ensure_cookie_file_netscape
  9534-9537   _ensure_notify_topic
 11635-11672  _ensure_proxy_ready
  9473-9496   _ensure_topic
   763-765    _env_int
   768-770    _env_int_range
 18368-18381  _event_webhook
 12964-12977  _evolution_loop
  6222-6256   _extract_file_payload
  1506-1517   _fanout_ziele
 26393-26456  _fatal_vom_botteil
 25047-25062  _fd_grenze_anheben
  5102-5112   _fehler_text
 11384-11402  _fetch_proxy_list
 18948-18976  _fetch_tiktok_room_id
   848-851    _ff_cmd
 19357-19370  _ffprobe_masse
 14006-14022  _fifo_schreiber_wecken
 13816-13821  _find_chromium
  3692-3694   _find_external_recorder
  2444-2446   _find_stream_urls
 12787-12812  _fire_webhooks
  8097-8107   _fork_safe
   953-966    _freeai_chat_sync_metered
  3959-3968   _get_ai_session
  7925-7965   _get_live_info
  3141-3148   _get_resolve_semaphore
  8622-9043   _handle_single_tracking
 25247-25249  _hb
 25252-25269  _hb_while
 20577-20588  _healthz_fuer_aufrufer
 25293-25321  _heap_zurueckgeben
 10997-11014  _herkunft_guard
 13231-13233  _highlight_cfg
 13236-13265  _highlight_observe
 13867-13875  _htmlov_bild_schreiben
 13845-13864  _htmlov_dauerbrowser
 13824-13842  _htmlov_screenshot_cmd
 18635-18645  _httpx_proxy
 12820-12832  _in_quiet_hours
 26217-26228  _init_db_oder_abbruch
 27070-27101  _install_fast_eventloop
 10545-10599  _install_fast_json
 12481-12497  _install_faulthandler
 20373-20382  _intel_ensure_schema
 20425-20460  _intel_index_loop
 20394-20409  _intel_index_one
 20385-20391  _intel_semantic
  5492-5505   _is_authorized
  8448-8469   _is_dead
  1967-1974   _is_process_running
  6848-6855   _is_quiet_hours
  1408-1417   _is_upload_window
  4967-4982   _iso
 10699-10708  _ist_lokal
 10634-10647  _json_error_handler
  4033-4052   _ki_nach_deckwahl
  4110-4119   _ki_rueckfall_melden
  8323-8330   _kick_cluster_gefunden
  8258-8320   _kick_cluster_weiter
  6897-6939   _kick_follower_count
  6881-6884   _kick_slug
  8228-8255   _kick_ws_pause
 26205-26214  _kickmod_boot
 25558-25561  _lagebild_discord_aufnahme
 25571-25575  _lagebild_kick_chat
 25564-25568  _lagebild_overlay
 25578-25580  _lagebild_spendenziel
 25545-25555  _lagebild_upload
 12849-12851  _latest_popularity
  1904-1913   _laufstand
 25733-25770  _laufstand_loop
 25171-25209  _leistung_erheben
  7814-7841   _link_video_senden
  8609-8620   _live_check_frist_melden
  2875-2888   _live_ohne_stream
 20010-20059  _live_react_loop
 19677-19999  _live_react_worker
  3540-3654   _live_status_aufloesen
 17750-17761  _live_transcript_push
 20001-20008  _live_users
 18219-18263  _living_title_loop
 22016-22088  _local_backup_scan
  4907-4930   _lock_update
 10616-10630  _log_5xx
 25212-25244  _log_schleuse_pruefen
   838-845    _log_sicher
 14509-14521  _looks_like_codec_err
 14504-14506  _looks_like_source_expired
  8146-8176   _loop_fehler
 12500-12509  _loop_heartbeat
 24953-24986  _loop_lag_monitor
 25000-25020  _loop_stockung_melden
 25023-25033  _loop_takt_starten
 12512-12585  _loop_watchdog_thread
 17627-17644  _loyalty_add
 17618-17624  _loyalty_get
 17647-17655  _loyalty_top
  5213-5232   _manual_status
  8471-8472   _mark_dead
 11855-11871  _marketing_loop
 23448-23466  _maybe_handle_command
 25872-25896  _maybe_hype_clip
 22422-22450  _meme_klassifizieren
 19274-19341  _meme_zusammenschnitt
  4451-4456   _migrate_columns
 23730-23741  _mod_is_exempt
 23744-23749  _mod_warn_first
 23752-23755  _mod_warn_text
 13006-13025  _modlog
 12989-13003  _modlog_schreiben
  1104-1106   _multistream_targets
  3325-3361   _nachschlag_ytdlp
  8110-8111   _nc_create_subprocess_exec
  8114-8115   _nc_create_subprocess_shell
 11969-11986  _news_loop
 13048-13050  _normalize_ingest
  2662-2679   _note_check_duration
  9528-9531   _notify_topic_name
  4055-4060   _nur_free
  4063-4067   _nur_free_sync
  4070-4107   _nur_lokal_sync
  2866-2872   _offline_ergebnis
  3364-3387   _ohne_url_melden
 17776-17784  _oracle_memories
 18071-18105  _oracle_memorize
 17787-17800  _oracle_persona
 17769-17773  _oracle_recent_text
 13440-13441  _ov_atomic_write
 13431-13433  _ov_bar
 16605-16617  _ov_clip_text
 13436-13437  _ov_oneline
 21403-21432  _overlay_push
 13770-13813  _overlay_render_size
 13117-13121  _overlay_session_reset
 21370-21372  _overlay_src_ok
 13450-13462  _overlay_takt
 16687-16697  _own_invites
 13765-13767  _parse_size
  7459-7492   _pause_resume_cmd
  2206-2250   _persist_refreshed_cookies
  2109-2141   _pick_checked_pull_proxy
 10765-10780  _pin_auth_value
 10869-10870  _pin_clear_fail
 10833-10836  _pin_global_gesperrt
 10786-10797  _pin_hmac_schluessel
 10839-10846  _pin_locked
 10849-10866  _pin_note_fail
 10800-10821  _pin_ok
 21198-21223  _piper_pick_model
 21283-21348  _piper_say
 12749-12784  _post_json_threaded
 13744-13762  _probe_video_size
  1995-2012   _proc_is_recorder
 11604-11632  _proxy_pool_refresh_loop
  2075-2106   _proxy_report_recording
  9182-9263   _pruef_runde
  9141-9179   _pruefstand_melden
 25082-25093  _pruefung_verworfen
 12466-12468  _prune_stall_dumps
  2272-2278   _pull_proxy_still
 18339-18365  _push_notify
 11061-11063  _pwa_dir
 11453-11470  _quick_validate_proxy
 12815-12817  _quiet_hours_config
 11026-11059  _rate_guard
  2891-2919   _raumsperre_fragen
 17588-17594  _react_warn
  8012-8051   _reap_proc
 10718-10734  _rebinding_melden
  9872-9939   _rec_auto_abschalten
  9819-9869   _rec_frueh_getrennt
  9684-9764   _rec_kategorie_melden
  9767-9816   _rec_totstreak_fortschreiben
  2702-2724   _record_check_outcome
   833-835    _redact_stream_urls
 11531-11601  _refresh_proxy_pool
  2479-2570   _resolve_via_html
  2922-3118   _resolve_via_webcast_api_v2
  3186-3273   _resolve_via_ytdlp
 23059-23188  _resolve_youtube_ingest
  2455-2476   _resolver_stumm
 13100-13111  _restream_active_sources
 14187-14314  _restream_avatar_feeder_start
 14317-14327  _restream_avatar_feeder_stop
 19431-19569  _restream_chat_guardian
 13268-13340  _restream_chat_push
 13417-13426  _restream_chat_push_async
 14025-14042  _restream_chatbild_start
 26100-26155  _restream_durchreicher
 13878-14003  _restream_html_overlay_start
 14045-14065  _restream_html_overlay_stop
 20311-20324  _restream_liste_abgleichen
 13059-13082  _restream_overlay_files
 20062-20094  _restream_platform_state
 20270-20305  _restream_resume_after_restart
 13371-13388  _restream_soll_schreiben
 13391-13414  _restream_status_schreiben
 14375-14447  _restream_tts_enqueue_wav
 13706-13738  _restream_tts_feeder
 13703-13704  _restream_tts_fifo_path
 14330-14357  _restream_tts_start
 14359-14373  _restream_tts_stop
 20100-20267  _restream_verify_loop
 21981-21993  _retention_loop
 21975-21978  _retention_scan
  2823-2825   _room_is_abo
  6259-6414   _run_ai_call
 12608-12621  _run_async_from_flask
 27059-27067  _run_selfcheck_and_exit
 21996-22007  _s3_client
  8498-8568   _safe_send
  5176-5192   _sample_net_throughput
 27039-27056  _sc_bericht
 26980-27036  _sc_dienste
 26887-26977  _sc_ki_und_stimme
 26838-26884  _sc_umgebung
  2768-2798   _schedule_next_check
 21929-21972  _scheduler_loop
  4459-4461   _schema_pk
 12624-12629  _scraper_session
 23758-23797  _screen_full
 12031-12068  _sec_headers
  2439-2441   _select_stream_from_data_section
 26748-26835  _selfcheck
  9540-9574   _send_live_notice
  1431-1435   _should_defer_upload
 22503-22541  _shrink_for_discord
 11066-11078  _sicheres_ziel
 21809-21847  _sicherheits_erinnerung_loop
 25793-25810  _sign_health_check
 25813-25832  _sign_health_loop
  4985-5010   _sitzung_bestimmen
 20560-20570  _sparen_lage
  8127-8138   _spawn
 27492-27522  _spawn_from_flask
 25096-25102  _speicher_maps
 25105-25120  _speicher_pflegen
 18647-18945  _start_chat_listener
 25065-25079  _start_gesperrt
 12588-12605  _start_loop_watchdog
 11917-11966  _stats_loop
 11896-11899  _stats_output_path
 11902-11914  _stats_write
 21235-21249  _stimme_saubern
 21256-21280  _stimme_schon_gesagt
  9122-9138   _storage_cleanup_loop
 25852-25859  _story_for
  3716-3722   _stream_url_expiry
  3724-3729   _stream_url_ttl
 16650-16657  _streamer_persona_get
 22113-22265  _system_backup
 22274-22304  _system_backup_loop
 12426-12444  _task_auf_bot_schleife
 24628-24644  _telegram_befehlsmenue
  8179-8225   _telegram_polling_fehler
  1476-1503   _telegram_ziele
 11405-11444  _test_proxy
 11827-11843  _testpush_resolve_live
 19352-19354  _text_schreiben
  7781-7789   _tg_botname
  7739-7778   _tg_ki_dialog
  9592-9602   _tg_migriert_laden
  9588-9589   _tg_migriert_pfad
  8474-8495   _tg_sprache_setzen
  9402-9412   _tg_topics_load_into_mem
  9399-9400   _tg_topics_path
  9414-9421   _tg_topics_save
 10737-10747  _token_ok
  9499-9515   _topic_anlegen
  9424-9431   _topic_forget
 12835-12846  _tracking_max_duration
  4721-4735   _tracking_remove_cleanup
  4752-4764   _tracking_resume_cleanup
  1806-1829   _try_attach_file_handler
 21225-21233  _tts_cleanup
 25517-25537  _tunnel_lage
 25678-25730  _tunnel_wacht_loop
 20728-20781  _twitch_channel_status
 23800-23948  _twitch_chat_loop
 22854-22867  _twitch_clip_versuchen
 23611-23717  _twitch_eventsub_loop
  1596-1631   _upload_queue_abarbeiten
  1454-1474   _upload_queue_add
  1567-1569   _upload_queue_count
  1437-1446   _upload_queue_load
  1634-1656   _upload_queue_nachher
  1427-1429   _upload_queue_path
  1553-1557   _upload_queue_remove
  1448-1452   _upload_queue_save
  1560-1565   _upload_queue_update
  9972-9996   _upload_rest_sichern
  1571-1593   _upload_window_loop
  7985-7992   _uptime_s
 13036-13045  _url_host
  3390-3488   _url_nachschlag
   913-917    _usage_record_claude
 25965-25987  _v37_pause_source
 25929-25939  _v37_restream_restart
 25942-25962  _v37_unpause_source
  8397-8441   _verbindung_verloren
  6942-6973   _viewer_sample_loop
 10873-10876  _wants_html
  7995-8009   _warn_empty_env
 25324-25449  _watchdog_loop
 23332-23340  _wchat_thank_ok
 25645-25675  _werkzeug_wacht_loop
 18407-18445  _whisper_get_model
  8086-8094   _whisper_native_section
 17575-17581  _whisper_pool
 18539-18571  _whisper_segments
 18447-18463  _whisper_stumm
 18466-18536  _whisper_transcribe
 13503-13660  _write_restream_overlay
 13465-13500  _write_restream_overlay_async
 23972-24071  _youtube_api_chat_loop
 20784-20887  _youtube_api_status
 20890-20957  _youtube_channel_status
 24074-24238  _youtube_chat_loop
 22870-22895  _youtube_clip_versuchen
 23194-23207  _youtube_restream_autoconfig
 23210-23234  _youtube_restream_autoconfig_inner
 23301-23329  _youtube_send
 21021-21062  _youtube_set_channel
 23237-23271  _yt_access_token
 23274-23289  _yt_live_chat_id
 23297-23298  _yt_sendrate_cfg
 23951-23966  _yt_timeout
  3165-3166   _ytdlp_detect_available
  3181-3183   _ytdlp_einzeln
  3168-3179   _ytdlp_note_result
 12471-12473  _zombie_child_count
 25155-25168  _zustand_kennzahlen
  7861-7885   about
  4640-4644   add_ai_log_entry
  5013-5084   add_recording
  4696-4713   add_tracking
  6417-6450   ai
  4210-4307   ai_chat
  4406-4416   ai_history_append
  4418-4423   ai_history_clear
  4395-4404   ai_history_load
  4380-4393   ai_rate_limit_check
  6479-6487   aireset
 17938-17957  azrael_chat
 24243-24346  brain_cmd
  3732-3737   build_recording_cmd
  4716-4719   bulk_add_trackings
  7212-7271   bulkadd
  9266-9382   check_all_trackings
  4767-4779   claim_live_transition
 16743-17507  class KickModerator
 14524-16493  class RestreamManager
  4933-4934   class _AufnahmeLockVerloren
  8333-8394   class _KickClusterSuche
 11715-11757  classify_proxy_anonymity
  6525-6724   cleanup
  5433-5439   cleanup_old_recordings
  4958-4965   clear_recording
 22898-22919  clip_moment
  7334-7410   cookies_cmd
  7413-7456   cookies_datei_cmd
  4687-4693   count_trackings_for_chat
  4627-4638   decide_preferred_recorder
  5917-6064   diag
 24510-24571  einnahmen_cmd
  4588-4604   finish_recording_attempt
  4740-4742   get_all_active_trackings
  5086-5089   get_all_recordings
  4566-4569   get_archive_entry
  2312-2317   get_cookie_health
  5156-5162   get_event_log
  4611-4625   get_last_recording_attempt
  3491-3533   get_live_status
  5167-5170   get_priority_poll_interval
  4606-4609   get_recent_recording_attempts
  5091-5094   get_recording_by_id
  3899-3928   get_redis
  5427-5431   get_storage_stats
  5206-5208   get_tiktok_status_distribution
  4781-4790   get_tracking_state
  4737-4738   get_trackings_for_group
 10060-10527  handle_recording_finished
 24620-24625  hilfe_cmd
  4474-4539   init_db
  5702-5740   live
  8571-8601   live_check_worker
  3983-4030   llm_chat
  4140-4181   llm_chat_sync
  4125-4137   llm_list_models
  5115-5148   log_event
  1929-1962   log_recording_failure
  7606-7655   logs_cmd
 26459-26738  main
  6453-6476   on_ai_media
  7732-7736   on_ai_reply
  7844-7858   on_azrael_mention
  7890-7920   on_callback
  9647-9665   on_chat_migration
  7798-7811   on_link_video
 17963-18068  oracle_handle
  7495-7498   pause_tracking
  5482-5487   profile_keyboard
  5655-5699   quelle
  7557-7603   quota
  9045-9119   reaper_loop
  5202-5204   record_tiktok_status
  6492-6522   recstatus
  3930-3938   redis_get_json
  3941-3947   redis_set_json
 24647-24657  report_cmd
 11760-11762  report_proxy_result
  2573-2615   resolve_tiktok_live_stream
  7501-7504   resume_tracking
 24660-24933  run_bot
 12323-12417  run_flask
  4647-4653   save_tiktok_check
  4937-4956   set_recording_file
  4745-4749   set_tracking_paused
 24605-24617  spenden_cmd
  9671-9682   split_and_send_video
  5565-5607   start
  4572-4586   start_recording_attempt
  6727-6765   stats
  5351-5404   stop_manual_recording
  7507-7554   stoprec
  6866-6874   summary_cmd
  7658-7729   sysres
  6066-6210   teststream
  5609-5650   tiktok
  7274-7331   topusers
  5777-5834   track
  5742-5774   track_exact
  5848-5915   tracklist
  5235-5349   trigger_manual_recording
  4869-4904   try_acquire_recording_lock
 24574-24602  unpause_cmd
  5836-5846   untrack
 24401-24507  update_cmd
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
abwehrlage.py          auswerten, configure, crowdsec_status, crowdsec_via_lapi, cscli_bin, cscli_path, darf_journal_lesen, ssh_angriffe, sudo_hinweis
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            aus_bestand, config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmechat.py        ass, ausschnitt, beenden, beginnen, clip_beginnt, clip_fertig, clip_merken, clips_nehmen, clips_offen, concat_liste, einbrennen_cmd, laeuft, modus, notieren, untertitel_cmd, zusammenschnitt_cmd
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest, stall_grenze
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, luecken, probe_cmd, sekunden, sitzung_id, tonformat, zieldatei
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
channels.py            chat_eintraege, configure_chat, restream_active, yt_sendrate_cfg
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
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwartung.py           faellig_in, letzter_lauf, merken, stand_datei
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, mariadb_lage, set_pool, treiber_fehler, treiber_wunsch, vorrat_groesse, vorrat_lage, vorrat_leeren
dcspar.py              anzeige, client_optionen, puffer
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordaufnahme.py     an, beschriftung, hochladen, teilen
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
discordziele.py        clip_kanal, clip_kanal_des_bereichs, clip_kanal_holen, eigene_kanaele, loeschbar, umzugsmarke, umzugsmarke_lesen
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
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
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
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
oeffentlichestats.py   configure, public_stats
outcomes.py            get_outcome_breakdown
overlaybrowser.py      browser_cmd, class Dauerbrowser, class OverlayBrowserFehler, lage, teilen
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
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
revenue.py             is_revenue_platform, normalisieren, sql_in
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
sicherungspruefung.py  archiv_lesbar, dump_vollstaendig, pruefen
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
telegramfehler.py      dashboard_umzug, dauer_text, ersatz, grund, ist_fehler, ist_telegram_chat, migration_plan, migriert_erlaubt, nur_telegram, standardgruppe, text, zuruecksetzen
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
uploadschlange.py      angekommen, faellig, gleicher, nach_versuch, pause_s
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
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
