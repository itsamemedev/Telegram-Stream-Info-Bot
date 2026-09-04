# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (42)

```
 10096  GET              /                                                dashboard
 12283  GET              /api/abo/status                                  api_abo_status
 12237  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10884  GET              /api/automation/status                           api_automation_status
 10906  POST             /api/automation/toggle                           api_automation_toggle
 19087  GET              /api/channel/categories                          api_channel_categories
 19093  POST             /api/channel/set                                 api_channel_set
 18940  GET              /api/channels/status                             api_channels_status
 18614  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 18597  GET              /api/clips                                       api_clips
 18643  POST/DELETE      /api/clips/clear                                 api_clips_clear
 18522  GET              /api/debug/threads                               api_debug_threads
 12248  GET              /api/events                                      api_events
 11710  GET              /api/events/stream                               api_events_stream
 11376  GET              /api/health                                      api_health
 18556  POST             /api/highlights/config                           api_highlights_config
 10030  POST             /api/login                                       dashboard_login_submit
 12576  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11625  GET              /api/notify/status                               api_notify_status
 11636  POST             /api/notify/test                                 api_notify_test
 12337  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12314  GET              /api/proxy/trend                                 api_proxy_trend
 20015  GET              /api/selftest                                    api_selftest
 11935  GET              /api/system                                      api_system
 12631  GET              /api/system/check_timing                         api_check_timing
 12723  GET              /api/system/config_drift                         api_config_drift
 11441  GET              /api/system/config_snapshot                      api_system_config_snapshot
 11483  GET              /api/system/preflight                            api_system_preflight
 11609  GET              /api/system/preflight_history                    api_system_preflight_history
 11775  GET              /api/system/resilience                           api_system_resilience
 18663  GET              /api/tts/<fn>                                    api_tts_file
 19389  GET              /api/upload_window                               api_upload_window
 11908  GET              /archive/<int:eid>/download                      archive_download
 11965  GET              /download/<int:recording_id>                     download
 11865  GET              /health                                          health
 18491  GET              /healthz                                         healthz
 10021  GET              /login                                           dashboard_login_page
 10051  GET              /logout                                          dashboard_logout
 10058  GET              /manifest.webmanifest                            pwa_manifest
 19362  GET              /overlay                                         overlay_page
 10082  GET              /pwa-icon-<variant>.png                          pwa_icon
 10068  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (317)

```
   182  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   389  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
  1003  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   743  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   874  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   854  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   892  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   816  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   551  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   649  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1241  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1273  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   340  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   956  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   936  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1109  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1157  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1208  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1067  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   911  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   375  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   639  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   521  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   504  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   496  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   332  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   348  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   683  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   648  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   668  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   555  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   216  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   241  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   246  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   406  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   397  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   286  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   208  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   174  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   157  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   366  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   343  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   193  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   130  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   115  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    92  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   153  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    79  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   161  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   410  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   284  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   269  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   192  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    70  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    77  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   464  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   213  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   240  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   200  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
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
   112  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   120  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   136  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   165  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   150  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   180  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   200  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   220  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   247  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   361  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   284  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   381  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   376  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   452  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   220  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   219  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   241  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   100  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   168  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   146  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   125  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   175  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
   395  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    69  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
    94  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   104  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    43  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    61  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
    91  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    57  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    68  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   133  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   128  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   119  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    44  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    83  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   267  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   334  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   362  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   213  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   280  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   515  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   178  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   161  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   401  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   225  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   177  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   460  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   435  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   296  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   142  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   832  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   914  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   942  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   953  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   819  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   881  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   868  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   849  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   314  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   494  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   489  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   537  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   420  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   747  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   511  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   474  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   447  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   721  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   591  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   680  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   586  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   519  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   299  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   764  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   387  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   642  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   797  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   782  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   343  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   581  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   567  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   550  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   607  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   700  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   596  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   486  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   464  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   505  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   522  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   574  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   440  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   596  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   535  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   561  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   134  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   144  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   325  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   315  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   350  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   333  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
   423  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   448  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   340  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   370  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
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
   206  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   356  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   176  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   238  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   453  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   482  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   402  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   415  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   511  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   388  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   263  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   308  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   332  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   319  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   165  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   277  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   135  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   369  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   424  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   252  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   463  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   429  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   488  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   468  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   451  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   444  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   238  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   305  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
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
   382  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands (45)

```
 20699  /ai                     
 21172  /ask                    
 20790  /assign_role            
 20836  /ban                    
 21504  /botstats               
 21428  /clearwarns             
 21468  /clip                   
 21453  /clipoftheweek          
 21295  /clips                  
 20751  /create_category        
 20720  /create_channel         
 20779  /create_group           
 20762  /create_role            
 20736  /create_voice           
 21072  /daily                  
 21202  /event                  
 21245  /events                 
 21341  /follow                 
 21325  /help                   
 20825  /kick                   
 21054  /leaderboard            
 21281  /livenow                
 21311  /post_test              
 21142  /profile                
 20860  /purge                  
 21040  /rank                   
 21268  /recstatus              
 20801  /remove_role            
 20713  /restream_status        
 20812  /set_channel_perms      
 21005  /setup_community        
 21023  /setup_targets          
 21367  /stats                  
 20625  /status                 
 21663  /streaminfo             
 21560  /sys_report             
 21536  /sys_unpause            
 20847  /timeout                
 21439  /topstreamers           
 20655  /track                  
 20639  /tracklist              
 21356  /unfollow               
 20688  /untrack                
 21389  /warn                   
 21413  /warnings               
```

## Discord-Events (4)

```
 22161  on_member_join
 22123  on_message
 21750  on_raw_reaction_add
 22196  on_ready
```

## Top-Level-Symbole in bot.py (483 Funktionen, 2 Klassen)

```
  2552-2553   _abo_key
  2573-2591   _abo_probe_dump
 19599-19609  _active_recorder_sync
 15651-15658  _ad_allowlist
 16792-16798  _agent_for
 19611-19629  _ai_calls_total_sync
 16801-16817  _ai_telemetry
 17306-17324  _alert
 22335-22385  _alert_monitor_loop
 22737-22799  _announce_loop
  3494-3497   _anthropic_key
  3504-3506   _anthropic_model
  9774-9777   _arg_int
  2544-2549   _as_dict
 17460-17482  _audio_tap_cmd
  9942-9953   _auth_cookie
  9909-9938   _auth_guard
  1715-1720   _auto_on
 18353-18371  _auto_restream_loop
 23878-23893  _azrael_broadcast_reply
 23778-23800  _azrael_chat_reply
 23761-23775  _azrael_chat_should_reply
 23806-23808  _azrael_gate_cfg
 16822-16836  _azrael_live_state
 19274-19288  _azrael_overlay_state
 17188-17242  _azrael_proactive_loop
 16640-16696  _azrael_reaction_to_chats
 23811-23818  _azrael_reply_all_chats
 23748-23758  _azrael_self_names
 23846-23875  _azrael_send_to
 16842-16863  _azrael_system
 22469-22472  _backup_active
 22550-22563  _backup_loop
 22274-22283  _brain_growth_loop
 10275-10302  _brain_growth_snapshot
  2480-2500   _brain_hint_delay
  6181-6209   _brain_notify
 11689-11706  _browser_push
  6225-6312   _build_daily_summary
  2983-3163   _build_native_cmd
 13837-14024  _build_restream_cmd
  3207-3240   _build_ytdlp_cmd
 19551-19558  _cached_probe
  5003-5030   _can_stop_tracking
  1895-1917   _capture_set_cookies
 12391-12394  _cfg_get
 12397-12399  _cfg_set
 19048-19083  _channel_set_all
 12995-12998  _chat_connected
 13001-13017  _chat_disconnected
  8260-8271   _chat_is_forum
 13037-13039  _chat_sanitize
 12980-12992  _chat_stat
 13020-13023  _chat_stats_snapshot
  3772-3783   _check_ai_alive_sync
  3786-3798   _check_ai_models_sync
 19560-19573  _check_redis_alive_sync
 19575-19595  _check_redis_version_sync
 10557-10600  _classify_pool_anonymity
 10603-10620  _classify_pool_anonymity_bg
   827-849    _claude_chat_sync_metered
  9803-9810   _client_ip
 22831-22858  _clip_prune
 22861-22871  _clip_recfile_for
 23412-23418  _clip_should_velocity
 22912-22994  _clip_to_discord
  3670-3679   _close_ai_session
 23924-23939  _cohost_broadcast
 23909-23910  _cohost_cfg
 23965-23977  _cohost_fire_highlight
 23913-23921  _cohost_gate
 23942-23962  _cohost_highlight
 23043-23105  _community_events_loop
 10205-10207  _conv_messages
  6584-6627   _cookie_alarm_loop
  1967-1971   _cookie_autorefresh_info
  1872-1876   _cookie_header
 11739-11771  _cpu_load_snapshot
  3992-4004   _create_index_safe
 19793-19899  _crowdsec_status
 19739-19790  _crowdsec_via_lapi
 19643-19661  _cscli_bin
 19670-19683  _cscli_path
  6474-6499   _daily_summary_loop
 19701-19718  _darf_journal_lesen
 22309-22332  _db_maintenance_loop
  6443-6471   _db_vacuum_loop
 15674-15698  _detect_foreign_ad
  1450-1461   _diag_path_owner
 17094-17138  _director_finalize
 17906-17913  _director_for
 17043-17091  _director_mark
 23306-23341  _disc_automod_check
 23282-23285  _disc_state_get
 23288-23295  _disc_state_set
 20275-20288  _discord_guild_filesize_bytes
 20482-20486  _discord_invite
 23243-23279  _discord_live_thread
 17245-17257  _discord_notify
 20381-20406  _discord_ops_alert
 23141-23239  _discord_post_user
 20542-22271  _discord_run_once
 20421-20479  _discord_start
 22802-22808  _discord_stop
 20296-20298  _discord_upload_limit_label
 20291-20293  _discord_upload_limit_mb
  6502-6579   _disk_alarm_loop
 25358-25407  _disk_autoclean
 25410-25423  _disk_guard_loop
 25350-25355  _disk_pct
 13430-13432  _drawtext_chain
 12069-12071  _dump_all_threads
 10483-10546  _enrich_proxies_with_geo
  2112-2156   _ensure_cookie_file_netscape
 20489-20539  _ensure_discord_invite
 23008-23040  _ensure_error_channel
  8319-8322   _ensure_notify_topic
 10727-10764  _ensure_proxy_ready
  8273-8300   _ensure_topic
   684-686    _env_int
   689-691    _env_int_range
 23108-23138  _error_channel_loop
 17290-17303  _event_webhook
 12810-12823  _evolution_loop
  5623-5657   _extract_file_payload
  2228-2230   _extract_urls_from_streamurl_node
 19686-19693  _f2b_sudo_hint
 17326-17328  _faster_whisper_available
  4503-4513   _fehler_text
 10384-10402  _fetch_proxy_list
 17740-17768  _fetch_tiktok_room_id
   760-763    _ff_cmd
 13596-13601  _find_chromium
  3200-3204   _find_external_recorder
  2233-2235   _find_stream_urls
 12442-12467  _fire_webhooks
  7364-7373   _fork_safe
   860-873    _freeai_chat_sync_metered
 19732-19736  _geo_lookup_ips
  3658-3667   _get_ai_session
  7197-7237   _get_live_info
  2770-2777   _get_resolve_semaphore
  7597-7974   _handle_single_tracking
 25176-25178  _hb
 25181-25198  _hb_while
 13051-13053  _highlight_cfg
 13056-13085  _highlight_observe
 13604-13622  _htmlov_screenshot_cmd
 17484-17494  _httpx_proxy
 12475-12487  _in_quiet_hours
 26249-26280  _install_fast_eventloop
  9669-9723   _install_fast_json
 12074-12090  _install_faulthandler
 18399-18408  _intel_ensure_schema
 18446-18481  _intel_index_loop
 18420-18430  _intel_index_one
 18411-18417  _intel_semantic
  4992-5001   _is_authorized
  7498-7504   _is_dead
  2218-2220   _is_hevc
 19721-19723  _is_private_ip
  1614-1621   _is_process_running
  6211-6222   _is_quiet_hours
  1251-1260   _is_upload_window
  9758-9771   _json_error_handler
  6437-6438   _kick_broadcaster_id
  6349-6391   _kick_follower_count
  6333-6336   _kick_slug
 11317-11348  _kick_user_token
  4041-4044   _kind_from_filename
 12504-12509  _latest_popularity
 18121-18154  _live_react_loop
 17917-18110  _live_react_worker
 16699-16710  _live_transcript_push
 18112-18119  _live_users
 17141-17185  _living_title_loop
  1793-1866   _load_cookies_dict
 22475-22547  _local_backup_scan
  9740-9754   _log_5xx
 14032-14044  _looks_like_codec_err
 14027-14029  _looks_like_source_expired
  7414-7444   _loop_fehler
 12094-12103  _loop_heartbeat
 25146-25173  _loop_lag_monitor
 12106-12174  _loop_watchdog_thread
 16579-16593  _loyalty_add
 16570-16576  _loyalty_get
 16596-16604  _loyalty_top
 12617-12619  _manual_donations_total
  4710-4729   _manual_status
  7506-7507   _mark_dead
 11003-11019  _marketing_loop
 23825-23843  _maybe_handle_command
 25509-25533  _maybe_hype_clip
  3959-3982   _migrate_columns
 24104-24115  _mod_is_exempt
 24118-24123  _mod_warn_first
 24126-24129  _mod_warn_text
 12850-12858  _modlog
  1002-1004   _multistream_targets
  7376-7377   _nc_create_subprocess_exec
  7380-7381   _nc_create_subprocess_shell
 11254-11271  _news_loop
 12877-12879  _normalize_ingest
  2411-2428   _note_check_duration
  8313-8316   _notify_topic_name
 16725-16733  _oracle_memories
 16998-17032  _oracle_memorize
 16736-16749  _oracle_persona
 16718-16722  _oracle_recent_text
 13211-13219  _ov_atomic_write
 13199-13205  _ov_bar
 15577-15589  _ov_clip_text
 13208-13209  _ov_oneline
 19326-19355  _overlay_push
 13550-13593  _overlay_render_size
 12943-12947  _overlay_session_reset
 19290-19293  _overlay_src_ok
 15661-15671  _own_invites
 13545-13547  _parse_size
 19907-19987  _parse_ssh_attacks
  6799-6832   _pause_resume_cmd
  1921-1965   _persist_refreshed_cookies
  1759-1791   _pick_checked_pull_proxy
  9839-9852   _pin_auth_value
  9898-9899   _pin_clear_fail
  9878-9881   _pin_locked
  9884-9895   _pin_note_fail
  9855-9875   _pin_ok
 19184-19209  _piper_pick_model
 19221-19268  _piper_say
 12404-12439  _post_json_threaded
 13524-13542  _probe_video_size
  1642-1659   _proc_is_recorder
 10696-10724  _proxy_pool_refresh_loop
  1725-1756   _proxy_report_recording
 12059-12061  _prune_stall_dumps
 11073-11194  _public_stats
 17261-17287  _push_notify
 10000-10002  _pwa_dir
 10453-10468  _quick_validate_proxy
 12470-12472  _quiet_hours_config
  9965-9998   _rate_guard
 16544-16550  _react_warn
  7284-7323   _reap_proc
  2451-2473   _record_check_outcome
   755-757    _redact_stream_urls
 10623-10693  _refresh_proxy_pool
  2244-2334   _resolve_via_html
  2593-2747   _resolve_via_webcast_api_v2
  2810-2872   _resolve_via_ytdlp
 23452-23581  _resolve_youtube_ingest
 12926-12937  _restream_active_sources
 17771-17870  _restream_chat_guardian
 13088-13160  _restream_chat_push
 13185-13194  _restream_chat_push_async
 13625-13712  _restream_html_overlay_start
 13715-13728  _restream_html_overlay_stop
 12888-12911  _restream_overlay_files
 18158-18190  _restream_platform_state
 18315-18350  _restream_resume_after_restart
 13776-13834  _restream_tts_enqueue_wav
 13486-13518  _restream_tts_feeder
 13483-13484  _restream_tts_fifo_path
 13731-13758  _restream_tts_start
 13760-13774  _restream_tts_stop
 18196-18312  _restream_verify_loop
 22440-22452  _retention_loop
 22434-22437  _retention_scan
  2555-2557   _room_is_abo
  5661-5778   _run_ai_call
 12197-12210  _run_async_from_flask
 19726-19729  _run_priv
 26237-26245  _run_selfcheck_and_exit
 22455-22466  _s3_client
  7533-7584   _safe_send
  4636-4652   _sample_net_throughput
  2503-2530   _schedule_next_check
 22388-22431  _scheduler_loop
  3985-3989   _schema_pk
 12214-12219  _scraper_session
 24132-24171  _screen_full
 11392-11429  _sec_headers
  2223-2225   _select_stream_from_data_section
 26050-26234  _selfcheck
  8325-8359   _send_live_notice
  1274-1278   _should_defer_upload
 22874-22909  _shrink_for_discord
 10005-10017  _sicheres_ziel
 22286-22306  _sicherheits_erinnerung_loop
 25430-25447  _sign_health_check
 25450-25469  _sign_health_loop
  7393-7404   _spawn
 26509-26539  _spawn_from_flask
 20008-20011  _st_befund
 17496-17737  _start_chat_listener
 12177-12194  _start_loop_watchdog
 11221-11249  _stats_loop
 11200-11203  _stats_output_path
 11206-11218  _stats_write
  8053-8069   _storage_cleanup_loop
 25489-25496  _story_for
  3262-3268   _stream_url_expiry
  3277-3283   _stream_url_is_fresh
  3270-3275   _stream_url_ttl
 15624-15631  _streamer_persona_get
 13435-13439  _studio_chain
 22572-22694  _system_backup
 22703-22733  _system_backup_loop
 10405-10444  _test_proxy
 10951-10967  _testpush_resolve_live
  7509-7530   _tg_sprache_setzen
  8232-8242   _tg_topics_load_into_mem
  8229-8230   _tg_topics_path
  8244-8251   _tg_topics_save
  9813-9821   _token_ok
  8254-8258   _topic_forget
 12490-12501  _tracking_max_duration
  4249-4263   _tracking_remove_cleanup
  4280-4292   _tracking_resume_cleanup
  1508-1531   _try_attach_file_handler
 19211-19219  _tts_cleanup
 10927-10931  _tunnel_effective
 18707-18760  _twitch_channel_status
 24174-24319  _twitch_chat_loop
 23988-24091  _twitch_eventsub_loop
  1297-1310   _upload_queue_add
  1321-1323   _upload_queue_count
  1280-1289   _upload_queue_load
  1270-1272   _upload_queue_path
  1312-1319   _upload_queue_remove
  1291-1295   _upload_queue_save
  1325-1366   _upload_window_loop
  7257-7264   _uptime_s
 12865-12874  _url_host
   735-752    _url_ohne_zugang
   820-824    _usage_record_claude
  7447-7491   _verbindung_verloren
  6394-6425   _viewer_sample_loop
  9902-9905   _wants_html
  7267-7281   _warn_empty_env
 25219-25340  _watchdog_loop
 23727-23735  _wchat_thank_ok
 17330-17360  _whisper_get_model
  7354-7361   _whisper_native_section
 16531-16537  _whisper_pool
 17429-17458  _whisper_segments
 17362-17426  _whisper_transcribe
 13266-13428  _write_restream_overlay
 13228-13263  _write_restream_overlay_async
 24343-24423  _youtube_api_chat_loop
 18763-18866  _youtube_api_status
 18869-18936  _youtube_channel_status
 24426-24587  _youtube_chat_loop
 23587-23600  _youtube_restream_autoconfig
 23603-23627  _youtube_restream_autoconfig_inner
 23694-23722  _youtube_send
 19004-19045  _youtube_set_channel
 23630-23664  _yt_access_token
 23667-23682  _yt_live_chat_id
 23690-23691  _yt_sendrate_cfg
 24322-24337  _yt_timeout
  2794-2795   _ytdlp_detect_available
  2797-2808   _ytdlp_note_result
 12064-12066  _zombie_child_count
  7133-7157   about
  4160-4164   add_ai_log_entry
  4077-4080   add_archive_entry
  4674-4676   add_archive_rule
  4451-4485   add_recording
  4224-4241   add_tracking
  5781-5814   ai
  3812-3863   ai_chat
  3897-3907   ai_history_append
  3909-3914   ai_history_clear
  3886-3895   ai_history_load
  3871-3884   ai_rate_limit_check
  5843-5851   aireset
 16866-16885  azrael_chat
 24592-24714  brain_cmd
  3286-3470   build_recording_cmd
  4244-4247   bulk_add_trackings
  6630-6689   bulkadd
  8072-8212   check_all_trackings
  4296-4308   claim_live_transition
 15701-16463  class KickModerator
 14047-15464  class RestreamManager
 10810-10852  classify_proxy_anonymity
  5889-6087   cleanup
  4928-4934   cleanup_old_recordings
  4442-4449   clear_recording
 23344-23409  clip_moment
  4626-4629   compute_storage_forecast
  6752-6796   cookies_cmd
  4215-4221   count_trackings_for_chat
  4147-4158   decide_preferred_recorder
  4087-4090   delete_archive_entry
  4678-4680   delete_archive_rule
  5318-5465   diag
 24826-24887  einnahmen_cmd
  4620-4623   find_recordings_by_fingerprint
  4108-4124   finish_recording_attempt
  4268-4270   get_all_active_trackings
  4175-4177   get_all_checks
  4487-4490   get_all_recordings
  4569-4571   get_all_tags_with_counts
  4597-4600   get_annotations_for_recording
  4082-4085   get_archive_entry
  4590-4593   get_bookmarked_recordings
  1988-2105   get_cookie_health
  4557-4563   get_event_log
  4131-4145   get_last_recording_attempt
  2875-2980   get_live_status
  4867-4870   get_manual_recordings
  4605-4608   get_or_compute_inspect_sync
  4969-4972   get_outcome_breakdown
  4576-4579   get_priority_poll_interval
  4126-4129   get_recent_recording_attempts
  4492-4495   get_recording_by_id
  4583-4586   get_recording_note
  3604-3627   get_redis
  4204-4207   get_stats
  4922-4926   get_storage_stats
  4698-4700   get_tiktok_status_distribution
  4310-4319   get_tracking_state
  4265-4266   get_trackings_for_group
  4883-4886   get_trash_recordings
  8980-9648   handle_recording_finished
  4007-4032   init_db
  4670-4672   list_archive_rules
  5122-5160   live
  7587-7595   live_check_worker
  3682-3716   llm_chat
  3739-3767   llm_chat_sync
  3724-3736   llm_list_models
  4516-4549   log_event
  1576-1609   log_recording_failure
  6946-6995   logs_cmd
 25537-26040  main
  5817-5840   on_ai_media
  7072-7098   on_ai_reply
  7101-7130   on_azrael_mention
  7162-7192   on_callback
 16891-16995  oracle_handle
  6835-6838   pause_tracking
  4982-4987   profile_keyboard
  6897-6943   quota
  7976-8050   reaper_loop
  4694-4696   record_tiktok_status
  5856-5886   recstatus
  3629-3637   redis_get_json
  3640-3646   redis_set_json
 24890-24900  report_cmd
 10855-10857  report_proxy_result
  2337-2364   resolve_tiktok_live_stream
  4878-4881   restore_recording
  6841-6844   resume_tracking
  4683-4688   run_archive_rules
 24903-25126  run_bot
 11979-12031  run_flask
  4658-4661   sample_bandwidth_for_active
  4167-4173   save_tiktok_check
  4434-4440   set_recording_file
  4273-4277   set_tracking_paused
  4873-4876   soft_delete_recording
  8365-8978   split_and_send_video
  5035-5077   start
  4092-4106   start_recording_attempt
  6090-6128   stats
  4848-4865   stop_manual_recording
  6847-6894   stoprec
  6318-6326   summary_cmd
  6998-7069   sysres
  5467-5611   teststream
  5079-5120   tiktok
  6692-6749   topusers
  5197-5254   track
  5162-5194   track_exact
  5268-5316   tracklist
  4732-4846   trigger_manual_recording
  4395-4432   try_acquire_recording_lock
  4889-4891   universal_search
  5256-5266   untrack
 24717-24823  update_cmd
  4615-4618   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
binresolve.py          resolve
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            geschuetzt, host, lage, nur_lokal, offen_im_netz
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_async, db_conn, get_pool, set_pool
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             broadcaster_id, configure, oauth_exchange, slug
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             changelog, current, latest, summary_line
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
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
