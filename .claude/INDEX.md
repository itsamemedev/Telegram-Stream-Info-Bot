# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 11173  GET              /                                                dashboard
 12779  GET              /api/abo/status                                  api_abo_status
 12735  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11866  GET              /api/automation/status                           api_automation_status
 11888  POST             /api/automation/toggle                           api_automation_toggle
 21177  GET              /api/channel/categories                          api_channel_categories
 21183  POST             /api/channel/set                                 api_channel_set
 21034  GET              /api/channels/status                             api_channels_status
 20736  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20719  GET              /api/clips                                       api_clips
 20765  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20673  GET              /api/debug/threads                               api_debug_threads
 12745  GET              /api/events                                      api_events
 12246  GET              /api/events/stream                               api_events_stream
 12109  GET              /api/health                                      api_health
 20704  POST             /api/highlights/config                           api_highlights_config
 11103  POST             /api/login                                       dashboard_login_submit
 13019  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12179  GET              /api/notify/status                               api_notify_status
 12190  POST             /api/notify/test                                 api_notify_test
 12833  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12810  GET              /api/proxy/trend                                 api_proxy_trend
 20783  GET              /api/tts/<fn>                                    api_tts_file
 21531  GET              /api/upload_window                               api_upload_window
 12348  GET              /archive/<int:eid>/download                      archive_download
 12374  GET              /download/<int:recording_id>                     download
 12307  GET              /health                                          health
 20545  GET              /healthz                                         healthz
 11094  GET              /login                                           dashboard_login_page
 11128  GET              /logout                                          dashboard_logout
 11135  GET              /manifest.webmanifest                            pwa_manifest
 21512  GET              /overlay                                         overlay_page
 11159  GET              /pwa-icon-<variant>.png                          pwa_icon
 11145  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (346)

```
   195  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   422  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
  1023  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   764  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   894  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   874  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   912  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   832  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   382  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   393  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   403  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   426  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   433  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   444  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   572  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   670  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1261  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1293  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   367  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   976  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   956  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1129  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1177  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1228  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1087  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   931  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
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
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
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
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   443  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   445  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   430  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   250  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   185  POST             /api/cookies/bereinigen                          api_cookies_bereinigen   [nc/routes/settings.py]
   130  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    71  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    78  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   497  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   271  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   298  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   391  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   335  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   353  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   258  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
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
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
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
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
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
   428  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
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
   229  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   212  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
   121  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   268  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   590  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   565  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   974  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1096  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1124  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1144  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   961  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1023  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1010  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   991  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   636  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   631  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   679  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   562  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   889  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   653  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   616  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   589  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   863  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   733  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   822  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   728  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   661  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   441  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   906  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   529  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   784  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   939  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   924  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   485  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   723  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   709  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   692  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   749  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1287  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1408  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1251  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   842  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   738  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   490  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   468  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   522  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   539  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   591  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   444  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   613  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   552  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   578  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   148  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   160  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   486  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   476  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   511  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
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
```

## Discord-Slash-Commands in discordbot.py (67)

```
  2247  /about                  Ueber diesen Bot
   981  /ai                     
  2247  /aireset                KI-Kontext zuruecksetzen
  1399  /ask                    
  1082  /assign_role            
  1132  /ban                    
  2203  /botstats               
  2247  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2247  /bulkadd                Mehrere User auf einmal tracken · a b c
  2247  /cleanup                Alte Aufnahmen aufraeumen
  1665  /clearwarns             
  2167  /clip                   
  2152  /clipoftheweek          
  1535  /clips                  
  2247  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1037  /create_category        
  1008  /create_channel         
  1072  /create_group           
  1047  /create_role            
  1023  /create_voice           
  1276  /daily                  
  2247  /diag                   Vollstaendige Diagnose
  2247  /einnahmen              Einnahmen und Spenden
  1428  /event                  
  1470  /events                 
  1575  /follow                 
  1564  /help                   
  1122  /kick                   
  1248  /leaderboard            
  2247  /live                   Live-Status sofort pruefen · @user
  1522  /livenow                
  2247  /logs                   Letzte Fehler aus dem Log
  2247  /pause                  Tracking pausieren · @user
  1550  /post_test              
  1360  /profile                
  1154  /purge                  
  2247  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2247  /quota                  Speicher-Quota
  1235  /rank                   
  1510  /recstatus              
  1092  /remove_role            
  2247  /report                 Azrael-Sentinel-Wochenreport
   994  /restream_status        
  2247  /resume                 Tracking fortsetzen · @user
  1102  /set_channel_perms      
  1197  /setup_community        
  1214  /setup_targets          
  1496  /spenden                
  1607  /stats                  
   953  /status                 
  2247  /stoprec                Laufende Aufnahme sauber beenden · @user
  1703  /streaminfo             
  2247  /summary                Tageszusammenfassung
  2247  /sysres                 System-Ressourcen
  2247  /teststream             Recorder-Selbsttest · @user
  2247  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1142  /timeout                
  1675  /topstreamers           
  2247  /topusers               Top-Streamer nach Aufnahmen
   883  /track                  
  2247  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   966  /tracklist              
  1589  /unfollow               
  2247  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   915  /untrack                
  1628  /warn                   
  1651  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2414  on_member_join
  2371  on_message
  2268  on_raw_reaction_add
  2449  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    60-75     konfiguriere
    78-533    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (54 Funktionen)

```
  1780-1831   _award_xp
   537-564    _bereich_umziehen
   484-494    _clip_kopieren
  2002-2031   _clip_week_leader
  2055-2069   _clipoftheweek_loop
  2566-2628   _community_events_loop
  1737-1759   _dc_client
  1762-1771   _dc_offen
  2668-2703   _disc_automod_check
   410-415    _disc_sprache_setzen
  1834-1882   _discord_ai_automod
   686-725    _discord_automod
  1885-1905   _discord_azrael_reply
  2072-2525   _discord_run_once
   245-303    _discord_start
   306-360    _ensure_discord_invite
  2531-2563   _ensure_error_channel
   431-444    _ensure_rank_roles
   846-860    _ensure_team_roles
  2631-2661   _error_channel_loop
   735-739    _guard
   655-683    _handle_voice_ai
   418-428    _is_admin
   509-534    _link_video
  1950-1961   _liveboard_loop
   742-775    _on_level_up
   651-652    _par_chat_id
  2034-2052   _post_clip_of_week
  1964-1982   _post_weekly_digest
   447-473    _provision_base_channels
  1502-1596   _reg_betrieb
  1168-1265   _reg_community_setup
  1268-1349   _reg_daily_profil
  1392-1489   _reg_frage_events
   940-996    _reg_info
  1114-1165   _reg_moderation
  1352-1389   _reg_profil
  1063-1111   _reg_rollen
   999-1060   _reg_server
  1492-1499   _reg_spenden
  1599-1686   _reg_streamer
  1689-1734   _reg_system
   874-937    _reg_tracking
   810-843    _run_tg_handler
   638-648    _tracked_usernames
   162-224    _uebernehmen
   497-506    _umzugsmarken
  1914-1947   _update_liveboard
  1985-1999   _weekly_digest_loop
   476-481    _ziel_guild
   567-609    _ziele_abgleichen
   618-635    _ziele_sync_loop
   612-615    _ziele_takt_min
   227-230    starte
```

## Top-Level-Symbole in bot.py (612 Funktionen, 4 Klassen)

```
 26615-26637  _abbruch_datenbank_unlesbar
  2822-2823   _abo_key
  2843-2861   _abo_probe_dump
 26737-26753  _abschied_wachen
 26756-26774  _abschluss
 16800-16807  _ad_allowlist
 17966-17972  _agent_for
 17975-17991  _ai_telemetry
 18507-18525  _alert
 22294-22344  _alert_monitor_loop
 19212-19269  _alte_beilagen_einsammeln
 22725-22787  _announce_loop
  3773-3783   _anthropic_key
  3786-3788   _anthropic_model
 10662-10665  _arg_int
  2814-2819   _as_dict
 26301-26310  _async_exc_handler
 18696-18718  _audio_tap_cmd
 19731-19790  _audio_tap_melden
 18732-18756  _audio_tap_sammler
 10011-10048  _aufnahme_beim_stopp_sichern
 19154-19175  _aufnahme_chat_ausklang
 19138-19151  _aufnahme_chat_beginnen
 19297-19318  _aufnahme_chat_dienst
 19491-19544  _aufnahme_chat_einarbeiten
 19133-19135  _aufnahme_chat_modus
 19321-19370  _aufnahme_chat_nachtrag
 19178-19209  _aufnahme_chat_vormerken
 19288-19294  _aufnahme_chat_wecken
 25426-25428  _aufnahme_deckel
 19373-19394  _aufnahme_fertigmachen
 22962-23015  _aufnahme_nach_discord
 10051-10069  _aufnahme_platz_frei
  9954-9981   _aufnahme_verteilen
 26701-26721  _aufnahmen_abschliessen
 26640-26698  _aufraeumen
 10936-11005  _auth_cookie
 10892-10932  _auth_guard
  2069-2074   _auto_on
 20416-20434  _auto_restream_loop
 14275-14317  _avatar_frames_laden
 16850-16863  _azrael_brain_kontext
 23919-23934  _azrael_broadcast_reply
 23819-23841  _azrael_chat_reply
 23791-23816  _azrael_chat_should_reply
 23847-23849  _azrael_gate_cfg
  4225-4238   _azrael_ki
 17994-18008  _azrael_live_state
  4241-4263   _azrael_lokal
 21427-21441  _azrael_overlay_state
 18050-18058  _azrael_persona_kern
 18389-18443  _azrael_proactive_loop
 17814-17870  _azrael_reaction_to_chats
 23852-23859  _azrael_reply_all_chats
  4266-4281   _azrael_schweigt_melden
 23778-23788  _azrael_self_names
 23887-23916  _azrael_send_to
 14236-14272  _azrael_spricht
 14583-14596  _azrael_stimme_stumm
 18014-18047  _azrael_system
 22428-22431  _backup_active
 22509-22522  _backup_loop
  5569-5592   _betreiber_pruefen
 25515-25519  _betrieb
 26374-26383  _brain_crowdsec_snap
 26542-26545  _brain_db_health
 22215-22224  _brain_growth_loop
 11307-11334  _brain_growth_snapshot
  2733-2767   _brain_hint_delay
 26446-26481  _brain_moderation_snap
  6842-6870   _brain_notify
 26548-26570  _brain_recording_snap
 26386-26443  _brain_restream_health
 26573-26586  _brain_tiktok_status_snap
 12225-12242  _browser_push
 14630-14634  _build_restream_cmd
  5595-5622   _can_stop_tracking
  2180-2202   _capture_set_cookies
 12885-12888  _cfg_get
 12891-12893  _cfg_set
 21138-21173  _channel_set_all
 13328-13331  _chat_connected
 13334-13350  _chat_disconnected
 19282-19285  _chat_einarbeiten_async
  9445-9475   _chat_is_forum
 19102-19127  _chat_listener_abbauen
  9617-9652   _chat_migriert
  9655-9656   _chat_migriert_async
 13370-13372  _chat_sanitize
 13313-13325  _chat_stat
 13353-13356  _chat_stats_snapshot
  4100-4112   _check_ai_models_sync
 11573-11616  _classify_pool_anonymity
   918-940    _claude_chat_sync_metered
 10694-10700  _client_ip
 23420-23434  _clip_chat_ass
 22871-22905  _clip_prune
 22908-22918  _clip_recfile_for
 23340-23408  _clip_schneiden
 23437-23443  _clip_should_velocity
 23018-23103  _clip_to_discord
 19462-19467  _clips_abwarten
  3973-3982   _close_ai_session
 23965-23980  _cohost_broadcast
 23950-23951  _cohost_cfg
 24006-24018  _cohost_fire_highlight
 23954-23962  _cohost_gate
 23983-24003  _cohost_highlight
 11268-11270  _conv_messages
  7176-7237   _cookie_alarm_loop
  2270-2271   _cookie_autofetch_info
  2254-2258   _cookie_autorefresh_info
 25976-25998  _cookie_bezug_loop
 26001-26026  _cookie_bezug_runde
  2157-2161   _cookie_header
 10703-10708  _cookie_sicher
  2283-2297   _cookies_selbst_holen
  4371-4373   _create_index_safe
 21777-21891  _crowdsec_status
 21723-21774  _crowdsec_via_lapi
 21634-21652  _cscli_bin
 21661-21674  _cscli_path
  7062-7089   _daily_summary_loop
 21692-21709  _darf_journal_lesen
  3299-3324   _darf_ytdlp_nachschlagen
 12389-12410  _dashboard_adresse
 10723-10727  _dashboard_hostnamen
  1522-1552   _dashboard_trackings_umziehen
 23411-23417  _datei_weg
 22268-22291  _db_maintenance_loop
  7012-7059   _db_vacuum_loop
 16823-16847  _detect_foreign_ad
  1750-1761   _diag_path_owner
 18294-18339  _director_finalize
 19721-19728  _director_for
 18243-18291  _director_mark
 23253-23256  _disc_state_get
 23259-23266  _disc_state_set
 22196-22205  _discord_bot_starten
 22159-22170  _discord_einladung_merken
 22208-22212  _discord_invite
 22173-22193  _discord_kontext
 23214-23250  _discord_live_thread
 18446-18458  _discord_notify
 22131-22156  _discord_ops_alert
 23114-23210  _discord_post_user
 22790-22796  _discord_stop
  7092-7173   _disk_alarm_loop
 25847-25898  _disk_autoclean
 26157-26170  _disk_guard_loop
 14215-14222  _drossel_hoeher
 14211-14212  _drossel_stufe
 14225-14233  _drossel_zuruecksetzen
 12566-12568  _dump_all_threads
 25522-25536  _einstellungen_startzeile
 11500-11563  _enrich_proxies_with_geo
  2322-2383   _ensure_cookie_file_netscape
  9546-9549   _ensure_notify_topic
 11723-11760  _ensure_proxy_ready
  9485-9508   _ensure_topic
   761-763    _env_int
   766-768    _env_int_range
 18491-18504  _event_webhook
 13111-13124  _evolution_loop
  6284-6318   _extract_file_payload
 21677-21684  _f2b_sudo_hint
  1508-1519   _fanout_ziele
 26777-26840  _fatal_vom_botteil
 25431-25446  _fd_grenze_anheben
  5037-5047   _fehler_text
 11401-11419  _fetch_proxy_list
 19071-19099  _fetch_tiktok_room_id
   846-849    _ff_cmd
 19475-19488  _ffprobe_masse
 14159-14175  _fifo_schreiber_wecken
 13969-13974  _find_chromium
  3694-3696   _find_external_recorder
  2446-2448   _find_stream_urls
 12934-12959  _fire_webhooks
  8109-8119   _fork_safe
   951-964    _freeai_chat_sync_metered
  3961-3970   _get_ai_session
  7937-7977   _get_live_info
  3143-3150   _get_resolve_semaphore
  8634-9055   _handle_single_tracking
 25631-25633  _hb
 25636-25653  _hb_while
 20658-20669  _healthz_fuer_aufrufer
 25677-25705  _heap_zurueckgeben
 11009-11026  _herkunft_guard
 13384-13386  _highlight_cfg
 13389-13418  _highlight_observe
 14020-14028  _htmlov_bild_schreiben
 13998-14017  _htmlov_dauerbrowser
 13977-13995  _htmlov_screenshot_cmd
 18758-18768  _httpx_proxy
 12967-12979  _in_quiet_hours
 26601-26612  _init_db_oder_abbruch
 27454-27485  _install_fast_eventloop
 10557-10611  _install_fast_json
 12571-12587  _install_faulthandler
 20454-20463  _intel_ensure_schema
 20506-20541  _intel_index_loop
 20475-20490  _intel_index_one
 20466-20472  _intel_semantic
  5554-5567   _is_authorized
  8460-8481   _is_dead
 21712-21714  _is_private_ip
  1969-1976   _is_process_running
  6872-6879   _is_quiet_hours
  1410-1419   _is_upload_window
  4902-4917   _iso
 10711-10720  _ist_lokal
 10646-10659  _json_error_handler
  4030-4039   _ki_rueckfall_melden
  7008-7009   _kick_broadcaster_id
  8335-8342   _kick_cluster_gefunden
  8270-8332   _kick_cluster_weiter
  6921-6963   _kick_follower_count
  6905-6908   _kick_slug
  8240-8267   _kick_ws_pause
 26589-26598  _kickmod_boot
  4454-4457   _kind_from_filename
 25942-25945  _lagebild_discord_aufnahme
 25955-25959  _lagebild_kick_chat
 25948-25952  _lagebild_overlay
 25962-25964  _lagebild_spendenziel
 25929-25939  _lagebild_upload
 12996-12998  _latest_popularity
  1906-1915   _laufstand
 26117-26154  _laufstand_loop
 25555-25593  _leistung_erheben
  7811-7838   _link_video_senden
  8621-8632   _live_check_frist_melden
  2877-2890   _live_ohne_stream
 20126-20175  _live_react_loop
 19793-20115  _live_react_worker
  3542-3656   _live_status_aufloesen
 17873-17884  _live_transcript_push
 20117-20124  _live_users
 18342-18386  _living_title_loop
 22434-22506  _local_backup_scan
  4842-4865   _lock_update
 10628-10642  _log_5xx
 25596-25628  _log_schleuse_pruefen
   836-843    _log_sicher
 14642-14654  _looks_like_codec_err
 14637-14639  _looks_like_source_expired
  8158-8188   _loop_fehler
 12590-12599  _loop_heartbeat
 25337-25370  _loop_lag_monitor
 25384-25404  _loop_stockung_melden
 25407-25417  _loop_takt_starten
 12602-12675  _loop_watchdog_thread
 17750-17767  _loyalty_add
 17741-17747  _loyalty_get
 17770-17778  _loyalty_top
  5237-5256   _manual_status
  8483-8484   _mark_dead
 11949-11965  _marketing_loop
 23866-23884  _maybe_handle_command
 26256-26280  _maybe_hype_clip
 22840-22868  _meme_klassifizieren
 19397-19459  _meme_zusammenschnitt
  4358-4363   _migrate_columns
 24148-24159  _mod_is_exempt
 24162-24167  _mod_warn_first
 24170-24173  _mod_warn_text
 13153-13172  _modlog
 13136-13150  _modlog_schreiben
  1106-1108   _multistream_targets
  3327-3363   _nachschlag_ytdlp
  8122-8123   _nc_create_subprocess_exec
  8126-8127   _nc_create_subprocess_shell
 12063-12080  _news_loop
 13195-13197  _normalize_ingest
  2664-2681   _note_check_duration
  9540-9543   _notify_topic_name
  2868-2874   _offline_ergebnis
  3366-3389   _ohne_url_melden
 17899-17907  _oracle_memories
 18194-18228  _oracle_memorize
 17910-17923  _oracle_persona
 17892-17896  _oracle_recent_text
 13593-13594  _ov_atomic_write
 13584-13586  _ov_bar
 16728-16740  _ov_clip_text
 13589-13590  _ov_oneline
 21476-21505  _overlay_push
 13923-13966  _overlay_render_size
 13264-13268  _overlay_session_reset
 21443-21445  _overlay_src_ok
 13603-13615  _overlay_takt
 16810-16820  _own_invites
 13918-13920  _parse_size
 21894-21974  _parse_ssh_attacks
  7487-7520   _pause_resume_cmd
  2208-2252   _persist_refreshed_cookies
  2111-2143   _pick_checked_pull_proxy
 10777-10792  _pin_auth_value
 10881-10882  _pin_clear_fail
 10845-10848  _pin_global_gesperrt
 10798-10809  _pin_hmac_schluessel
 10851-10858  _pin_locked
 10861-10878  _pin_note_fail
 10812-10833  _pin_ok
 21271-21296  _piper_pick_model
 21356-21421  _piper_say
 12896-12931  _post_json_threaded
 13897-13915  _probe_video_size
  1997-2014   _proc_is_recorder
 11692-11720  _proxy_pool_refresh_loop
  2077-2108   _proxy_report_recording
  9194-9275   _pruef_runde
  9153-9191   _pruefstand_melden
 25466-25477  _pruefung_verworfen
 12556-12558  _prune_stall_dumps
  2274-2280   _pull_proxy_still
 18462-18488  _push_notify
 11073-11075  _pwa_dir
 11470-11485  _quick_validate_proxy
 12962-12964  _quiet_hours_config
 11038-11071  _rate_guard
  2893-2921   _raumsperre_fragen
 17711-17717  _react_warn
  8024-8063   _reap_proc
 10730-10746  _rebinding_melden
  9884-9951   _rec_auto_abschalten
  9831-9881   _rec_frueh_getrennt
  9696-9776   _rec_kategorie_melden
  9779-9828   _rec_totstreak_fortschreiben
  2704-2726   _record_check_outcome
   831-833    _redact_stream_urls
 11619-11689  _refresh_proxy_pool
  2481-2572   _resolve_via_html
  2924-3120   _resolve_via_webcast_api_v2
  3188-3275   _resolve_via_ytdlp
 23477-23606  _resolve_youtube_ingest
  2457-2478   _resolver_stumm
 13247-13258  _restream_active_sources
 14320-14447  _restream_avatar_feeder_start
 14450-14460  _restream_avatar_feeder_stop
 19547-19685  _restream_chat_guardian
 13421-13493  _restream_chat_push
 13570-13579  _restream_chat_push_async
 26484-26539  _restream_durchreicher
 14031-14156  _restream_html_overlay_start
 14178-14198  _restream_html_overlay_stop
 13206-13229  _restream_overlay_files
 20178-20210  _restream_platform_state
 20378-20413  _restream_resume_after_restart
 13524-13541  _restream_soll_schreiben
 13544-13567  _restream_status_schreiben
 14508-14580  _restream_tts_enqueue_wav
 13859-13891  _restream_tts_feeder
 13856-13857  _restream_tts_fifo_path
 14463-14490  _restream_tts_start
 14492-14506  _restream_tts_stop
 20216-20375  _restream_verify_loop
 22399-22411  _retention_loop
 22393-22396  _retention_scan
  2825-2827   _room_is_abo
  6321-6438   _run_ai_call
 12698-12711  _run_async_from_flask
 21717-21720  _run_priv
 27443-27451  _run_selfcheck_and_exit
 22414-22425  _s3_client
  8510-8580   _safe_send
  5168-5184   _sample_net_throughput
 27423-27440  _sc_bericht
 27364-27420  _sc_dienste
 27271-27361  _sc_ki_und_stimme
 27222-27268  _sc_umgebung
  2770-2800   _schedule_next_check
 22347-22390  _scheduler_loop
  4366-4368   _schema_pk
 12714-12719  _scraper_session
 24176-24215  _screen_full
 12125-12162  _sec_headers
  2441-2443   _select_stream_from_data_section
 27132-27219  _selfcheck
  9552-9586   _send_live_notice
  1433-1437   _should_defer_upload
 22921-22959  _shrink_for_discord
 11078-11090  _sicheres_ziel
 22227-22265  _sicherheits_erinnerung_loop
 26177-26194  _sign_health_check
 26197-26216  _sign_health_loop
  4920-4945   _sitzung_bestimmen
 20641-20651  _sparen_lage
  8139-8150   _spawn
 27873-27903  _spawn_from_flask
 25480-25486  _speicher_maps
 25489-25504  _speicher_pflegen
 18770-19068  _start_chat_listener
 25449-25463  _start_gesperrt
 12678-12695  _start_loop_watchdog
 12011-12060  _stats_loop
 11990-11993  _stats_output_path
 11996-12008  _stats_write
 21308-21322  _stimme_saubern
 21329-21353  _stimme_schon_gesagt
  9134-9150   _storage_cleanup_loop
 26236-26243  _story_for
  3718-3724   _stream_url_expiry
  3726-3731   _stream_url_ttl
 16773-16780  _streamer_persona_get
 22531-22683  _system_backup
 22692-22722  _system_backup_loop
 12516-12534  _task_auf_bot_schleife
 25013-25029  _telegram_befehlsmenue
  8191-8237   _telegram_polling_fehler
  1478-1505   _telegram_ziele
 11422-11461  _test_proxy
 11921-11937  _testpush_resolve_live
 19470-19472  _text_schreiben
  9604-9614   _tg_migriert_laden
  9600-9601   _tg_migriert_pfad
  8486-8507   _tg_sprache_setzen
  9414-9424   _tg_topics_load_into_mem
  9411-9412   _tg_topics_path
  9426-9433   _tg_topics_save
 10749-10759  _token_ok
  9511-9527   _topic_anlegen
  9436-9443   _topic_forget
 12982-12993  _tracking_max_duration
  4656-4670   _tracking_remove_cleanup
  4687-4699   _tracking_resume_cleanup
  1808-1831   _try_attach_file_handler
 21298-21306  _tts_cleanup
 11905-11909  _tunnel_effective
 25901-25921  _tunnel_lage
 26062-26114  _tunnel_wacht_loop
 20801-20854  _twitch_channel_status
 24218-24366  _twitch_chat_loop
 23272-23285  _twitch_clip_versuchen
 24029-24135  _twitch_eventsub_loop
  1598-1633   _upload_queue_abarbeiten
  1456-1476   _upload_queue_add
  1569-1571   _upload_queue_count
  1439-1448   _upload_queue_load
  1636-1658   _upload_queue_nachher
  1429-1431   _upload_queue_path
  1555-1559   _upload_queue_remove
  1450-1454   _upload_queue_save
  1562-1567   _upload_queue_update
  9984-10008  _upload_rest_sichern
  1573-1595   _upload_window_loop
  7997-8004   _uptime_s
 13183-13192  _url_host
  3392-3490   _url_nachschlag
   911-915    _usage_record_claude
 26349-26371  _v37_pause_source
 26313-26323  _v37_restream_restart
 26326-26346  _v37_unpause_source
  8409-8453   _verbindung_verloren
  6966-6997   _viewer_sample_loop
 10885-10888  _wants_html
  8007-8021   _warn_empty_env
 25708-25833  _watchdog_loop
 23750-23758  _wchat_thank_ok
 26029-26059  _werkzeug_wacht_loop
 18530-18568  _whisper_get_model
  8098-8106   _whisper_native_section
 17698-17704  _whisper_pool
 18662-18694  _whisper_segments
 18570-18586  _whisper_stumm
 18589-18659  _whisper_transcribe
 13656-13813  _write_restream_overlay
 13618-13653  _write_restream_overlay_async
 24390-24489  _youtube_api_chat_loop
 20857-20960  _youtube_api_status
 20963-21030  _youtube_channel_status
 24492-24656  _youtube_chat_loop
 23288-23313  _youtube_clip_versuchen
 23612-23625  _youtube_restream_autoconfig
 23628-23652  _youtube_restream_autoconfig_inner
 23719-23747  _youtube_send
 21094-21135  _youtube_set_channel
 23655-23689  _yt_access_token
 23692-23707  _yt_live_chat_id
 23715-23716  _yt_sendrate_cfg
 24369-24384  _yt_timeout
  3167-3168   _ytdlp_detect_available
  3183-3185   _ytdlp_einzeln
  3170-3181   _ytdlp_note_result
 12561-12563  _zombie_child_count
 25539-25552  _zustand_kennzahlen
  7873-7897   about
  4567-4571   add_ai_log_entry
  4484-4487   add_archive_entry
  5201-5203   add_archive_rule
  4948-5019   add_recording
  4631-4648   add_tracking
  6441-6474   ai
  4121-4216   ai_chat
  4313-4323   ai_history_append
  4325-4330   ai_history_clear
  4302-4311   ai_history_load
  4287-4300   ai_rate_limit_check
  6503-6511   aireset
 18061-18080  azrael_chat
 24661-24783  brain_cmd
  3734-3739   build_recording_cmd
  4651-4654   bulk_add_trackings
  7240-7299   bulkadd
  9278-9394   check_all_trackings
  4702-4714   claim_live_transition
 16866-17630  class KickModerator
 14657-16616  class RestreamManager
  4868-4869   class _AufnahmeLockVerloren
  8345-8406   class _KickClusterSuche
 11803-11845  classify_proxy_anonymity
  6549-6748   cleanup
  5491-5497   cleanup_old_recordings
  4893-4900   clear_recording
 23316-23337  clip_moment
  5159-5162   compute_storage_forecast
  7362-7438   cookies_cmd
  7441-7484   cookies_datei_cmd
  4622-4628   count_trackings_for_chat
  4554-4565   decide_preferred_recorder
  4494-4497   delete_archive_entry
  5205-5207   delete_archive_rule
  5979-6126   diag
 24895-24956  einnahmen_cmd
  5153-5156   find_recordings_by_fingerprint
  4515-4531   finish_recording_attempt
  4675-4677   get_all_active_trackings
  4582-4584   get_all_checks
  5021-5024   get_all_recordings
  5102-5104   get_all_tags_with_counts
  5130-5133   get_annotations_for_recording
  4489-4492   get_archive_entry
  5123-5126   get_bookmarked_recordings
  2314-2319   get_cookie_health
  5091-5097   get_event_log
  4538-4552   get_last_recording_attempt
  3493-3535   get_live_status
  5430-5433   get_manual_recordings
  5138-5141   get_or_compute_inspect_sync
  5531-5534   get_outcome_breakdown
  5109-5112   get_priority_poll_interval
  4533-4536   get_recent_recording_attempts
  5026-5029   get_recording_by_id
  5116-5119   get_recording_note
  3901-3930   get_redis
  4611-4614   get_stats
  5485-5489   get_storage_stats
  5225-5227   get_tiktok_status_distribution
  4716-4725   get_tracking_state
  4672-4673   get_trackings_for_group
  5446-5449   get_trash_recordings
 10072-10539  handle_recording_finished
 25005-25010  hilfe_cmd
  4381-4446   init_db
  5197-5199   list_archive_rules
  5764-5802   live
  8583-8613   live_check_worker
  3985-4027   llm_chat
  4060-4092   llm_chat_sync
  4045-4057   llm_list_models
  5050-5083   log_event
  1931-1964   log_recording_failure
  7634-7683   logs_cmd
 26843-27122  main
  6477-6500   on_ai_media
  7760-7786   on_ai_reply
  7841-7870   on_azrael_mention
  7902-7932   on_callback
  9659-9677   on_chat_migration
  7795-7808   on_link_video
 18086-18191  oracle_handle
  7523-7526   pause_tracking
  5544-5549   profile_keyboard
  5717-5761   quelle
  7585-7631   quota
  9057-9131   reaper_loop
  5221-5223   record_tiktok_status
  6516-6546   recstatus
  3932-3940   redis_get_json
  3943-3949   redis_set_json
 25032-25042  report_cmd
 11848-11850  report_proxy_result
  2575-2617   resolve_tiktok_live_stream
  5441-5444   restore_recording
  7529-7532   resume_tracking
  5210-5215   run_archive_rules
 25045-25317  run_bot
 12413-12507  run_flask
  4574-4580   save_tiktok_check
  4872-4891   set_recording_file
  4680-4684   set_tracking_paused
  5436-5439   soft_delete_recording
 24990-25002  spenden_cmd
  9683-9694   split_and_send_video
  5627-5669   start
  4499-4513   start_recording_attempt
  6751-6789   stats
  5375-5428   stop_manual_recording
  7535-7582   stoprec
  6890-6898   summary_cmd
  7686-7757   sysres
  6128-6272   teststream
  5671-5712   tiktok
  7302-7359   topusers
  5839-5896   track
  5804-5836   track_exact
  5910-5977   tracklist
  5259-5373   trigger_manual_recording
  4804-4839   try_acquire_recording_lock
  5452-5454   universal_search
 24959-24987  unpause_cmd
  5898-5908   untrack
 24786-24892  update_cmd
  5148-5151   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
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
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatnachtrag.py        beilage_lesen, beilage_zu, eingearbeitet, ensure_schema, erledigt, fehlversuch, ist_beilage, lesen, offene, stempel, unveraendert, vormerken
chatstats.py           summarize
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
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      anzeige_groesse, avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
forkriegel.py          class Vortritt
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
gegendruck.py          abgewiesen, deckel_auto, fd_grenze_anheben, fd_lage, freigeben, lage, reservieren, reserviert, start_entscheiden, verworfen, zuruecksetzen
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
geschuetzt.py          lage, ruhend, vermerken, verschlossen, zuruecksetzen
heapzaum.py            arenen_wunsch, deckeln, lage, rss_mb, takt_min, zurueckgeben
herkunft.py            entscheiden
highlights.py          check, new_state, observe, score, zustand
httpsitzung.py         schliessen, sitzung, teilen
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          einwertig, prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, state_gueltig, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, naechster_cluster, naechster_key, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
kickzentrifugo.py      als_frame, antwort_fehler, class KickZentrifugoFehler, connect_cmd, fehler_code, ist_ping, kanal, lage, neue_client_id, neues_token, pause, refresh_cmd, subscribe_cmd, token_aus, ttl_aus, verbindung_body, ws_url_aus, zerlegen, zugang
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              azrael_lage, azrael_wahl, backend, gesamtzeit, llm_zeiten, lokal_installiert, lokal_stand, lokal_zuerst, lokales_modell, normal, provider, vorrang, wartezeit, weg_zaehlen, zeitlimit
lagebild.py            bauen, dienst_quelle, dienste, dienste_lesen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
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
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, ein_start_je_ziel, fenstergroesse, freigeben, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, startend, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, bruecke, bruecke_luecke, bruecke_offline, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, fueller, quell_eingang, schriftart, zubringer
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              anlegen, create_schema, index_sicher, kollation_angleichen, modultabellen, parameter, spalten_nachziehen
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
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
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
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
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
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
